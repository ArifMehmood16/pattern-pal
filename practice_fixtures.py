import json

class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def make_list(values):
    dummy = tail = ListNode()
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next

def list_values(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values

def cycle_list(values, position):
    head = make_list(values)
    nodes, node = [], head
    while node:
        nodes.append(node)
        node = node.next
    if position >= 0:
        nodes[-1].next = nodes[position]
    return head

def check_trie(Trie):
    trie = Trie()
    trie.insert('apple')
    assert trie.search('apple') and not trie.search('app') and trie.starts_with('app')
    trie.insert('app')
    return trie.search('app') and not trie.starts_with('banana')


def check_min_stack(MinStack):
    s=MinStack();s.push(-2);s.push(0);s.push(-3)
    assert s.get_min()==-3
    assert s.pop()==-3
    return s.top()==0 and s.get_min()==-2

def check_moving_average(MovingAverage):
    m=MovingAverage(3)
    return m.next(1)==1 and m.next(10)==5.5 and m.next(3)==14/3 and m.next(5)==6

def check_lca(function):
    left=TreeNode(2,TreeNode(4),TreeNode(5))
    root=TreeNode(1,left,TreeNode(3))
    return function(root,left.left,left.right) is left
