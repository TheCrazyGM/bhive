from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
#: Operation ids
ops = [
    'vote',
    'comment',
    'transfer',
    'transfer_to_vesting',
    'withdraw_vesting',
    'limit_order_create',
    'limit_order_cancel',
    'feed_publish',
    'convert',
    'account_create',
    'account_update',
    'witness_update',
    'account_witness_vote',
    'account_witness_proxy',
    'pow',
    'custom',
    'report_over_production',
    'delete_comment',
    'custom_json',
    'comment_options',
    'set_withdraw_vesting_route',
    'limit_order_create2',
    'claim_account',
    'create_claimed_account',
    'request_account_recovery',
    'recover_account',
    'change_recovery_account',
    'escrow_transfer',
    'escrow_dispute',
    'escrow_release',
    'pow2',
    'escrow_approve',
    'transfer_to_savings',
    'transfer_from_savings',
    'cancel_transfer_from_savings',
    'custom_binary',
    'decline_voting_rights',
    'reset_account',
    'set_reset_account',
    'claim_reward_balance',
    'delegate_vesting_shares',
    'account_create_with_delegation',
    'witness_set_properties',
    'account_update2',
    'create_proposal',
    'update_proposal_votes',
    'remove_proposal',    
    'fill_convert_request',
    'author_reward',
    'curation_reward',
    'comment_reward',
    'liquidity_reward',
    'producer_reward',
    'interest',
    'fill_vesting_withdraw',
    'fill_order',
    'shutdown_witness',
    'fill_transfer_from_savings',
    'hardfork',
    'comment_payout_update',
    'return_vesting_delegation',
    'comment_benefactor_reward',
    'return_vesting_delegation',
    'comment_benefactor_reward',
    'producer_reward',
    'clear_null_account_balance',
    'proposal_pay',
    'hps_fund'
]
operations = {o: ops.index(o) for o in ops}

ops_wls = [
    'vote',
    'comment',
    'transfer',
    'transfer_to_vesting',
    'withdraw_vesting',
    'account_create',
    'account_update',
    'account_action',
    'social_action',
    'witness_update',
    'account_witness_vote',
    'account_witness_proxy',
    'custom',
    'delete_comment',
    'custom_json',
    'comment_options',
    'set_withdraw_vesting_route',
    'custom_binary',
    'claim_reward_balance',
    'friend_action',
    'pod_action',
    'author_reward',
    'curation_reward',
    'comment_reward',
    'shutdown_witness',
    'hardfork',
    'comment_payout_update',
    'comment_benefactor_reward',
    'devfund',
    'pod_virtual'
]
operations_wls = {o: ops_wls.index(o) for o in ops_wls}


def getOperationNameForId(i):
    """ Convert an operation id into the corresponding string
    """
    for key in operations:
        if int(operations[key]) is int(i):
            return key
    return "Unknown Operation ID %d" % i
