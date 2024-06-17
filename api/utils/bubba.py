import pandas as pd
import os
def run_panda():
    # change file paths if needed
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, 'vertex_tokens.csv')
    tokens = pd.read_csv(csv_file_path)
    tokens.token_symbol = tokens.token_symbol.str.upper()

    csv = 1
    if csv:
        message_file_path = os.path.join(current_dir, 'message.txt')
        dump = pd.read_csv(message_file_path, header=None)
        dump = dump[dump[25] != 'HYPERLIQUID']

        one = pd.Series(dump[0], name='stv_id')
        two = pd.Series(dump[34].str.upper().map(str) + "-" + dump[41].map(str), name='token_symbol')
    else:
        dump = pd.read_json('/content/drive/MyDrive/STFX/Arbitrum Incentives/stv-registry.stv.vaults.json')
        dump = dump[dump['protocol'] != 'HYPERLIQUID']

        one = pd.Series(dump["_id"], name='stv_id')
        two = pd.Series(dump['target_asset'].str.upper().map(str) + "-" + dump['trade_type'].map(str), name='token_symbol')

    vaults = pd.DataFrame(
        [one, two]
    ).transpose()

    vaults['token_address'] = vaults['token_symbol'].map(dict(zip(tokens['token_symbol'], tokens['token_address'])))

    vaults.to_csv('vault.csv', index=False)
    vaults