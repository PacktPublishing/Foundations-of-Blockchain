from boa.interop.Neo.Runtime import Log, Notify
from boa.interop.Neo.Storage import Get, Put, GetContext
from boa.interop.Neo.Runtime import GetTrigger,CheckWitness
from boa.builtins import concat


def main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No asset id supplied")
        return 0

    if operation == 'query':
        asset_id = args[0]
        return query_asset(asset_id)

    elif operation == 'delete':
        asset_id = args[0]
        return delete_asset(asset_id)

    elif operation == 'register':
        if nargs < 2:
            print("required arguments: [asset_id] [owner]")
            return 0
        asset_id = args[0]
        owner = args[1]
        return register_asset(asset_id, owner)

    elif operation == 'transfer':
        if nargs < 2:
            print("required arguments: [asset_id] [to_address]")
            return 0
        asset_id = args[0]
        to_address = args[1]
        return transfer_asset(asset_id, to_address)


def query_asset(asset_id):
    msg = concat("QueryAsset: ", asset_id)
    Notify(msg)

    context = GetContext()
    owner = Get(context, asset_id)
    if not owner:
        Notify("Asset is not yet registered")
        return False

    Notify(owner)
    return owner


def register_asset(asset_id, owner):
    msg = concat("RegisterAsset: ", asset_id)
    Notify(msg)

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the sender")
        return False

    context = GetContext()
    exists = Get(context, asset_id)
    if exists:
        Notify("Asset is already registered")
        return False

    Put(context, asset_id, owner)
    return True


def transfer_asset(asset_id, to_address):
    msg = concat("TransferAsset: ", asset_id)
    Notify(msg)

    context = GetContext()
    owner = Get(context, asset_id)
    if not owner:
        Notify("Asset is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot transfer")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner address. Must be exactly 34 characters")
        return False

    Put(context, asset_id, to_address)
    return True


def delete_asset(asset_id):
    msg = concat("DeleteAsset: ", asset_id)
    Notify(msg)

    context = GetContext()
    owner = Get(context, asset_id)
    if not owner:
        Notify("Asset is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot transfer")
        return False

    Delete(context, asset_id)
    return True