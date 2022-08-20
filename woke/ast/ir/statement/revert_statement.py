from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, Iterator, Optional, Union

from woke.ast.enums import ModifiesStateFlag
from woke.ast.ir.abc import IrAbc, SolidityAbc
from woke.ast.ir.expression.function_call import FunctionCall
from woke.ast.ir.statement.abc import StatementAbc
from woke.ast.ir.utils import IrInitTuple
from woke.ast.nodes import SolcRevertStatement

if TYPE_CHECKING:
    from .block import Block
    from .do_while_statement import DoWhileStatement
    from .for_statement import ForStatement
    from .if_statement import IfStatement
    from .unchecked_block import UncheckedBlock
    from .while_statement import WhileStatement


class RevertStatement(StatementAbc):
    _ast_node: SolcRevertStatement
    _parent: Union[
        Block,
        DoWhileStatement,
        ForStatement,
        IfStatement,
        UncheckedBlock,
        WhileStatement,
    ]

    __error_call: FunctionCall
    __documentation: Optional[str]

    def __init__(
        self, init: IrInitTuple, revert: SolcRevertStatement, parent: SolidityAbc
    ):
        super().__init__(init, revert, parent)
        self.__error_call = FunctionCall(init, revert.error_call, self)
        self.__documentation = revert.documentation

    def __iter__(self) -> Iterator[IrAbc]:
        yield self
        yield from self.__error_call

    @property
    def parent(
        self,
    ) -> Union[
        Block,
        DoWhileStatement,
        ForStatement,
        IfStatement,
        UncheckedBlock,
        WhileStatement,
    ]:
        return self._parent

    @property
    def error_call(self) -> FunctionCall:
        return self.__error_call

    @property
    def documentation(self) -> Optional[str]:
        return self.__documentation

    @property
    @lru_cache(maxsize=None)
    def modifies_state(self) -> ModifiesStateFlag:
        return self.error_call.modifies_state
