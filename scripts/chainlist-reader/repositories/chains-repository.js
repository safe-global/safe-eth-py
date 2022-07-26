const { readdir, readFile } = require('fs/promises');

/**
 * Formats chain names to the expected format (uppercase, _ separator).
 * @param {String} name chain name to format.
 * @returns {String} formatted chain name.
 */
const formatChainName = (name) => (name
  ? name.toUpperCase().replaceAll(' ', '_').replaceAll('-', '_')
  : 'null');

/**
 * Gets the chains data for every JSON file in the repository.
 * @param {String} basePath base path to read the chains data.
 * @returns {{String, String}} object containing chain ids and names.
 */
const getAllChains = async (basePath) => {
  const files = await readdir(`${basePath}/_data/chains`);

  return Promise.all(files.map(async (file) => {
    const content = await readFile(`${basePath}/_data/chains/${file}`);
    const data = JSON.parse(content);

    return {
      id: data?.chainId,
      name: formatChainName(data?.name),
    };
  }));
};

module.exports = {
  getAllChains,
};
