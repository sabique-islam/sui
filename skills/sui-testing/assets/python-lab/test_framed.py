"""Runnable pytest/Hypothesis example; no network or customer data."""
import pytest
from hypothesis import given, settings, strategies as st
from framed import encode, decode

@settings(max_examples=100,derandomize=True,database=None)
@given(st.binary(max_size=64))
def test_roundtrip(payload):
    assert decode(encode(payload))==payload

@pytest.mark.parametrize('packet',[b'',b'\x02a',b'\x00extra',b'\x41'+b'a'*65])
def test_rejects_bad_length(packet):
    with pytest.raises(ValueError):decode(packet)

def test_empty_payload_is_a_real_frame():
    assert encode(b'')==b'\x00'
    assert decode(b'\x00')==b''
