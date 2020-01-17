#!/bin/bash
#
# """
# 按照资产hostname进行自动分配到对应规则的节点下
# 规则：
#     Hostname: dw-prd-sns-community_api_service-55-instanceid
#     Node: Default/prd/sns/ 
# 
#     Hostname: dw-prd-order-community_api_service-56-insstanceid
#     Node: Default/prd/order/ 
# 
# 
# Author: Jiangjie Bai
# Email: jiangjie.bai@fit2cloud.com
# """

function grouping_asset() {

python3 ../apps/manage.py shell << EOF

from assets.models import Asset

class GroupingAsset(object):

    def __init__(self):
        self.separator = '-'

    def get_all_assets(self):
        from assets.models import Asset
        return Asset.objects.all()

    def get_or_create_node(self, node_value, parent_node=None):
        from assets.models import Node
        if parent_node is None:
            node = Node.objects.get(value=node_value)
            return node

        node = parent_node.children.filter(value=node_value).first()
        if not node:
            node = parent_node.create_child(value=node_value)
        return node

    def get_except_node(self, asset):
        old_hostname_list = asset.hostname.split(self.separator)
        new_hostname_list = old_hostname_list[:-3]
        new_hostname_list[0] = 'Default'
        parent_node = None
        for node_value in new_hostname_list:
            node = self.get_or_create_node(node_value, parent_node)
            parent_node = node
        return node

    def get_default_node(self):
        from assets.models import Node
        return Node.objects.get(value='Default')

    def move_asset_to_node(self, asset, node):
        print("----- Move asset {} to node {}. Old nodes: {}".format(asset.hostname, node.full_value, [_node.full_value for _node in asset.nodes.all()]))
        default_node = self.get_default_node()
        asset.nodes.set([node])
        asset.nodes.remove(default_node)

    def perform(self):
        assets = self.get_all_assets()
        print("Need move asset count: {}".format(assets.count()))
        for asset in assets:
            try:
                node = self.get_except_node(asset)
                self.move_asset_to_node(asset, node)
            except Exception as e:
                print("----- Error: {} - {}".format(asset, e))

GroupingAsset().perform()

EOF
}

grouping_asset
