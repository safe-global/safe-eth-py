import django_filters

from .forms import EthereumAddressFieldForm, Keccak256FieldForm


class EthereumAddressFilter(django_filters.Filter):
    field_class = EthereumAddressFieldForm


class Keccak256Filter(django_filters.Filter):
    field_class = Keccak256FieldForm
