from unittest.mock import Mock

from webob.multidict import MultiDict

from pyramid_tutorial.forms import ProductForm


def test_product_form__empty():
    form = ProductForm()
    assert form.validate() is False
    assert len(form.errors) == 2
    assert 'name' in form.errors
    assert 'status' in form.errors


def test_product_form__long_name():
    form = ProductForm(MultiDict([('name', 'a' * 101), ('status', '0')]))
    assert form.validate() is False
    assert len(form.errors) == 1
    assert 'name' in form.errors


def test_product_form__populate_obj():
    form = ProductForm(MultiDict([('name', 'a' * 10), ('status', '0')]))
    assert form.validate() is True
    product = Mock()
    form.populate_obj(product)
    assert product.name == 'aaaaaaaaaa'
    assert product.status == 0
