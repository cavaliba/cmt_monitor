import pytest
import sys
sys.path.insert(0, './cmt')
import globals as cmt
import args

# {'cron': False, 'report': False, 'pager': False, 
# 'persist': False, 'conf': None, 'modules': [[]], 
# 'listmodules': False, 'available': False, 'pagertest': False, 
# 'no_pager_rate_limit': False, 'checkconfig': False, 'version': False, 
# 'debug': False, 'debug2': False, 'devmode': False, 'short': False}

def test_parser_empty():

    r = args.parse_arguments([])
    assert r['cron'] is False
    assert r['short'] is False
    assert r['persist'] is False

def test_parser_cron():

    r = args.parse_arguments(['--cron'])
    assert r['cron'] is True

def test_parser_help():

    with pytest.raises(SystemExit):
        r = args.parse_arguments(['-h'])

def test_parser_is_module_allowed():

    cmt.ARGS = args.parse_arguments(['url', 'cpu'])

    assert args.is_module_allowed_in_args('url') is True
    assert args.is_module_allowed_in_args('cpu') is True
    assert args.is_module_allowed_in_args('swap') is False


def test_parser_is_module_list_valid_in_args():

    cmt.ARGS = args.parse_arguments(['url', 'cpu'])
    assert args.is_module_list_valid_in_args() is True

    #cmt.ARGS = args.parse_arguments(['bad_module'])
    #assert args.is_module_list_valid_in_args() is False, "bad_module not checked: " + str(cmt.ARGS)