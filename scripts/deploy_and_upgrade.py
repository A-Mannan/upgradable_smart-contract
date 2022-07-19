from brownie import (
    Box,
    BoxV2,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    network,
    Contract,
)
from scripts.helpful_scripts import get_account, encode_function_data, upgrade


def main():
    account = get_account()
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"]
    )
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account}
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(f"value in the Box set to {proxy_box.retrieve()}")
    box_v2 = BoxV2.deploy({"from": account})
    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(f"value incremented to {proxy_box.retrieve()}")