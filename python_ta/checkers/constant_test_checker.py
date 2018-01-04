"""
checker for using constant value in a conditional statement
"""
import astroid

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages


class UsingConstantTestChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = 'using-constants-test'

    msgs = {'W7777': ('using a constant value in a conditional statement'
                      , 'using-constants-test'
                      , 'Conditional statements should depend on a variable not a constant value.'
                        'This is usually not what the user intended to do'),}

    # this is important so that your checker is executed before others
    priority = -1

    def _check_all_constants(self, node):
        """
        Precondition: node is a condition in an if statement
        Returns true if all values in the BinOp tree are constants or if all values in the UnaryOp tree are constants
        Returns false otherwise
        Used in check_if_constant to check for constant test in BinOp/UnaryOp/Const nodes
        """
        if isinstance(node, astroid.Const):
            return True
        elif isinstance(node, astroid.BinOp):
            return self._check_all_constants(node.left) and self._check_all_constants(node.right)
        elif isinstance(node, astroid.UnaryOp):
            return self._check_all_constants(node.operand)
        elif isinstance(node, astroid.BoolOp):
            constant = True
            for each in node.values:
                constant = constant and self._check_all_constants(each)
            return constant
        else:
            return False

    @check_messages("using-constants-test")
    def visit_if(self, node):
        # check if node is a conditional statement
        if self._check_all_constants(node.test):
            self.add_message('using-constants-test', node=node.test)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(UsingConstantTestChecker(linter))