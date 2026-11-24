use pyo3::buffer::PyUntypedBuffer;
use pyo3::exceptions::{PyBufferError, PyTypeError, PyValueError};
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::critical_section::{with_critical_section, with_critical_section2};
use pyo3::types::{PyBytes, PyInt, PyMemoryView, PyString};
use secp256k1::Message;
use secp256k1::ecdsa::{RecoverableSignature, RecoveryId};
use tiny_keccak::{Hasher, Keccak};

const ADDRESS_LENGTH: usize = 20;
const HEX_ADDRESS_LENGTH: usize = 40;
/// Same threshold as `hashlib` and pysha3: smaller inputs hash faster than the cost of
/// releasing and taking back the GIL
const KECCAK_RELEASE_GIL_MIN_LENGTH: usize = 2048;

fn keccak256_digest(data: &[u8]) -> [u8; 32] {
    let mut hasher = Keccak::v256();
    let mut digest = [0u8; 32];
    hasher.update(data);
    hasher.finalize(&mut digest);
    digest
}

/// Python int to 32 bytes big endian. `None` if it is negative or does not fit.
fn int_to_be_bytes32(value: &Bound<'_, PyInt>) -> Option<[u8; 32]> {
    // `int.to_bytes(value, ...)`, so an `int` subclass cannot change the conversion
    let py = value.py();
    let be_bytes_object = py
        .get_type::<PyInt>()
        .call_method1(intern!(py, "to_bytes"), (value, 32, intern!(py, "big")))
        .ok()?;
    let be_bytes = be_bytes_object.cast::<PyBytes>().ok()?;
    be_bytes.as_bytes().try_into().ok()
}

/// Ethereum `v` (27 or 28) to the recovery id (y parity of the `R` point)
fn recovery_id_from_v(v: &Bound<'_, PyInt>) -> Option<RecoveryId> {
    match v.extract::<u64>().ok()? {
        27 => Some(RecoveryId::Zero),
        28 => Some(RecoveryId::One),
        _ => None,
    }
}

fn recover_address(
    message_hash: &[u8; 32],
    recovery_id: RecoveryId,
    r: &[u8; 32],
    s: &[u8; 32],
) -> Option<[u8; ADDRESS_LENGTH]> {
    let mut compact_signature = [0u8; 64];
    compact_signature[..32].copy_from_slice(r);
    compact_signature[32..].copy_from_slice(s);
    let signature = RecoverableSignature::from_compact(&compact_signature, recovery_id).ok()?;
    let public_key = signature
        .recover_ecdsa(Message::from_digest(*message_hash))
        .ok()?;
    let digest = keccak256_digest(&public_key.serialize_uncompressed()[1..]);
    let mut address = [0u8; ADDRESS_LENGTH];
    address.copy_from_slice(&digest[32 - ADDRESS_LENGTH..]);
    Some(address)
}

/// Recover the signer address of an Ethereum ECDSA signature over a 32 bytes hash,
/// with the input rules of the EVM `ecrecover` precompile: `v` must be 27 or 28,
/// `r` and `s` in `[1, n - 1]`, and high `s` values are accepted.
///
/// Returns the 20 bytes address, or `None` if no address can be recovered.
/// Raises `ValueError` if `message_hash` is not 32 bytes.
#[pyfunction]
fn ecrecover<'py>(
    py: Python<'py>,
    message_hash: &[u8],
    v: &Bound<'py, PyInt>,
    r: &Bound<'py, PyInt>,
    s: &Bound<'py, PyInt>,
) -> PyResult<Option<Bound<'py, PyBytes>>> {
    let message_hash: [u8; 32] = message_hash
        .try_into()
        .map_err(|_| PyValueError::new_err("message_hash must be 32 bytes"))?;
    let (Some(recovery_id), Some(r), Some(s)) = (
        recovery_id_from_v(v),
        int_to_be_bytes32(r),
        int_to_be_bytes32(s),
    ) else {
        return Ok(None);
    };
    let address = py.detach(|| recover_address(&message_hash, recovery_id, &r, &s));
    Ok(address.map(|address| PyBytes::new(py, &address)))
}

fn verify_p256(
    message_hash: &[u8; 32],
    r: &[u8; 32],
    s: &[u8; 32],
    public_key_x: &[u8; 32],
    public_key_y: &[u8; 32],
) -> bool {
    use p256::Sec1Point;
    use p256::ecdsa::signature::hazmat::PrehashVerifier;
    use p256::ecdsa::{Signature, VerifyingKey};

    let Ok(signature) = Signature::from_scalars(*r, *s) else {
        return false;
    };
    let public_key_point =
        Sec1Point::from_affine_coordinates(&(*public_key_x).into(), &(*public_key_y).into(), false);
    let Ok(verifying_key) = VerifyingKey::from_sec1_point(&public_key_point) else {
        return false;
    };
    verifying_key
        .verify_prehash(message_hash, &signature)
        .is_ok()
}

/// Verify a `secp256r1` (P-256) ECDSA signature over a 32 bytes digest, with the rules of
/// the RIP-7212 / EIP-7951 `P256VERIFY` precompile: `r` and `s` in `[1, n - 1]`, the public
/// key a point on the curve, and high `s` values accepted.
///
/// Returns `False` for any value out of range, and raises `TypeError` if a value is not an `int`.
#[pyfunction]
fn p256_verify(
    py: Python<'_>,
    message_hash: &Bound<'_, PyInt>,
    r: &Bound<'_, PyInt>,
    s: &Bound<'_, PyInt>,
    public_key_x: &Bound<'_, PyInt>,
    public_key_y: &Bound<'_, PyInt>,
) -> bool {
    let (Some(message_hash), Some(r), Some(s), Some(public_key_x), Some(public_key_y)) = (
        int_to_be_bytes32(message_hash),
        int_to_be_bytes32(r),
        int_to_be_bytes32(s),
        int_to_be_bytes32(public_key_x),
        int_to_be_bytes32(public_key_y),
    ) else {
        return false;
    };
    py.detach(|| verify_p256(&message_hash, &r, &s, &public_key_x, &public_key_y))
}

fn keccak256_digest_releasing_gil(py: Python<'_>, data: &[u8]) -> [u8; 32] {
    if data.len() >= KECCAK_RELEASE_GIL_MIN_LENGTH {
        py.detach(|| keccak256_digest(data))
    } else {
        keccak256_digest(data)
    }
}

/// Keccak-256 digest (Ethereum flavour, not NIST SHA3-256) of the raw bytes of `bytes` or of
/// any other C-contiguous buffer (`bytearray`, `memoryview`, `array`...), like `hashlib`.
///
/// Raises `TypeError` for an object that is not a buffer, and `BufferError` for a buffer
/// that is not C-contiguous.
#[pyfunction]
fn keccak256<'py>(py: Python<'py>, data: &Bound<'py, PyAny>) -> PyResult<Bound<'py, PyBytes>> {
    if let Ok(data_bytes) = data.cast::<PyBytes>() {
        let digest = keccak256_digest_releasing_gil(py, data_bytes.as_bytes());
        return Ok(PyBytes::new(py, &digest));
    }
    let buffer = PyUntypedBuffer::get(data)
        .map_err(|_| PyTypeError::new_err("Expected bytes or another object with a buffer"))?;
    if !buffer.is_c_contiguous() {
        return Err(PyBufferError::new_err("Expected a C-contiguous buffer"));
    }
    // Other threads can write to a mutable buffer while it is hashed, so it is copied first,
    // holding the object lock that a `bytearray` also takes to change its content on
    // free-threaded Python. For a `memoryview` that is the lock of the object it exposes
    let mut data_copy = vec![0u8; buffer.len_bytes()];
    if !data_copy.is_empty() {
        let copy_buffer = || {
            // SAFETY: `buffer` is held until the end of the function, so its `len_bytes`
            // C-contiguous bytes at `buf_ptr` stay allocated
            unsafe {
                std::ptr::copy_nonoverlapping(
                    buffer.buf_ptr().cast::<u8>(),
                    data_copy.as_mut_ptr(),
                    data_copy.len(),
                );
            }
        };
        let memory_view_object = data
            .cast::<PyMemoryView>()
            .ok()
            .and_then(|memory_view| memory_view.getattr(intern!(py, "obj")).ok())
            .filter(|memory_view_object| !memory_view_object.is_none());
        match memory_view_object {
            Some(memory_view_object) => {
                with_critical_section2(data, &memory_view_object, copy_buffer)
            }
            None => with_critical_section(data, copy_buffer),
        }
    }
    let digest = keccak256_digest_releasing_gil(py, &data_copy);
    Ok(PyBytes::new(py, &digest))
}

/// Lowercase hex of the address, without `0x`. `None` if `address_bytes` is not 20 bytes.
fn lowercase_hex_from_bytes(address_bytes: &[u8]) -> Option<[u8; HEX_ADDRESS_LENGTH]> {
    const HEX_DIGITS: &[u8; 16] = b"0123456789abcdef";
    if address_bytes.len() != ADDRESS_LENGTH {
        return None;
    }
    let mut lowercase_hex = [0u8; HEX_ADDRESS_LENGTH];
    for (index, byte) in address_bytes.iter().enumerate() {
        lowercase_hex[index * 2] = HEX_DIGITS[(byte >> 4) as usize];
        lowercase_hex[index * 2 + 1] = HEX_DIGITS[(byte & 0x0f) as usize];
    }
    Some(lowercase_hex)
}

/// Lowercase hex of the address, without `0x`. `None` if `address_text` is not 40 ASCII hex
/// characters in any case, with an optional `0x`/`0X` prefix.
fn lowercase_hex_from_text(address_text: &str) -> Option<[u8; HEX_ADDRESS_LENGTH]> {
    let hex_digits = address_text
        .strip_prefix("0x")
        .or_else(|| address_text.strip_prefix("0X"))
        .unwrap_or(address_text)
        .as_bytes();
    if hex_digits.len() != HEX_ADDRESS_LENGTH {
        return None;
    }
    let mut lowercase_hex = [0u8; HEX_ADDRESS_LENGTH];
    for (index, character) in hex_digits.iter().enumerate() {
        if !character.is_ascii_hexdigit() {
            return None;
        }
        lowercase_hex[index] = character.to_ascii_lowercase();
    }
    Some(lowercase_hex)
}

/// EIP-55 checksum of a lowercase hex address, `0x` prefixed.
fn checksum_from_lowercase_hex(lowercase_hex: &[u8; HEX_ADDRESS_LENGTH]) -> [u8; 42] {
    let address_hash = keccak256_digest(lowercase_hex);
    let mut checksum_address = [0u8; 42];
    checksum_address[0] = b'0';
    checksum_address[1] = b'x';
    for (index, character) in lowercase_hex.iter().enumerate() {
        let hash_nibble = if index % 2 == 0 {
            address_hash[index / 2] >> 4
        } else {
            address_hash[index / 2] & 0x0f
        };
        checksum_address[index + 2] = if hash_nibble > 7 {
            character.to_ascii_uppercase()
        } else {
            *character
        };
    }
    checksum_address
}

/// EIP-55 checksum address from 20 bytes, or from 40 hex characters in any case with an
/// optional `0x`/`0X` prefix.
///
/// Raises `ValueError` if `value` is not an address, and `TypeError` if it is not `bytes`
/// or `str`.
#[pyfunction]
fn to_checksum_address<'py>(
    py: Python<'py>,
    value: &Bound<'py, PyAny>,
) -> PyResult<Bound<'py, PyString>> {
    let lowercase_hex = if let Ok(address_bytes) = value.cast::<PyBytes>() {
        lowercase_hex_from_bytes(address_bytes.as_bytes())
    } else if let Ok(address_text) = value.cast::<PyString>() {
        address_text.to_str().ok().and_then(lowercase_hex_from_text)
    } else {
        return Err(PyTypeError::new_err("Expected bytes or str"));
    }
    .ok_or_else(|| PyValueError::new_err("Expected 20 bytes or a 40 characters hex address"))?;
    let checksum_address = checksum_from_lowercase_hex(&lowercase_hex);
    // Only ASCII hex digits and `0x` are written above
    let checksum_text = std::str::from_utf8(&checksum_address).expect("ASCII address");
    Ok(PyString::new(py, checksum_text))
}

/// `True` if `value` is a `0x` prefixed EIP-55 checksum address. `False` for any other
/// value, including other types.
#[pyfunction]
fn is_checksum_address(value: &Bound<'_, PyAny>) -> bool {
    let Some(address_text) = value
        .cast::<PyString>()
        .ok()
        .and_then(|address_text| address_text.to_str().ok())
    else {
        return false;
    };
    address_text.starts_with("0x")
        && lowercase_hex_from_text(address_text).is_some_and(|lowercase_hex| {
            checksum_from_lowercase_hex(&lowercase_hex) == address_text.as_bytes()
        })
}

// No shared mutable state, so the module runs on free-threaded Python without the GIL
#[pymodule(gil_used = false)]
fn safe_eth_native(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(ecrecover, module)?)?;
    module.add_function(wrap_pyfunction!(p256_verify, module)?)?;
    module.add_function(wrap_pyfunction!(keccak256, module)?)?;
    module.add_function(wrap_pyfunction!(to_checksum_address, module)?)?;
    module.add_function(wrap_pyfunction!(is_checksum_address, module)?)?;
    Ok(())
}
