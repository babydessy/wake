from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from wake.core.enums import EvmVersionEnum
from wake.utils import StrEnum

__doc__ = """Solc standard JSON input data model as described by https://docs.soliditylang.org/en/v0.8.12/using-the-compiler.html#input-description"""


class SolcInputLanguageEnum(StrEnum):
    SOLIDITY = "Solidity"
    YUL = "Yul"


class SolcStopAfterEnum(StrEnum):
    PARSING = "parsing"


class MetadataBytecodeHashEnum(StrEnum):
    NONE = "none"
    IPFS = "ipfs"
    BZZR1 = "bzzr1"


class SolcOutputSelectionEnum(StrEnum):
    AST = "ast"
    ABI = "abi"
    DEVDOC = "devdoc"
    """Developer documentation (natspec)"""
    USERDOC = "userdoc"
    """User documentation (natspec)"""
    METADATA = "metadata"
    IR = "ir"
    """Yul intermediate representation of the code before optimization"""
    IR_AST = "irAst"
    """AST of Yul intermediate representation of the code before optimization"""
    IR_OPTIMIZED = "irOptimized"
    """Intermediate representation after optimization"""
    IR_OPTIMIZED_AST = "irOptimizedAst"
    """AST of intermediate representation after optimization"""
    STORAGE_LAYOUT = "storageLayout"
    """Slots, offsets and types of the contract's state variables"""
    EVM_ALL = "evm"
    """All EVM subassets"""
    EVM_ASSEMBLY = "evm.assembly"
    """New assembly format"""
    EVM_LEGACY_ASSEMBLY = "evm.legacyAssembly"
    """Old-style assembly format in JSON"""
    EVM_BYTECODE_ALL = "evm.bytecode"
    """All bytecode subassets"""
    EVM_BYTECODE_FUNCTION_DEBUG_DATA = "evm.bytecode.functionDebugData"
    """Debugging information at function level"""
    EVM_BYTECODE_OBJECT = "evm.bytecode.object"
    """Bytecode object"""
    EVM_BYTECODE_OPCODES = "evm.bytecode.opcodes"
    """Opcodes list"""
    EVM_BYTECODE_SOURCE_MAP = "evm.bytecode.sourceMap"
    """Source mapping (useful for debugging)"""
    EVM_BYTECODE_LINK_REFERENCES = "evm.bytecode.linkReferences"
    """Link references (if unlinked object)"""
    EVM_BYTECODE_GENERATED_SOURCES = "evm.bytecode.generatedSources"
    """Sources generated by the compiler"""
    EVM_DEPLOYED_BYTECODE_ALL = "evm.deployedBytecode"
    """All deployed bytecode subassets"""
    EVM_DEPLOYED_BYTECODE_FUNCTION_DEBUG_DATA = "evm.deployedBytecode.functionDebugData"
    """Debugging information at function level"""
    EVM_DEPLOYED_BYTECODE_OBJECT = "evm.deployedBytecode.object"
    """Bytecode object"""
    EVM_DEPLOYED_BYTECODE_OPCODES = "evm.deployedBytecode.opcodes"
    """Opcodes list"""
    EVM_DEPLOYED_BYTECODE_SOURCE_MAP = "evm.deployedBytecode.sourceMap"
    """Source mapping (useful for debugging)"""
    EVM_DEPLOYED_BYTECODE_LINK_REFERENCES = "evm.deployedBytecode.linkReferences"
    """Link references (if unlinked object)"""
    EVM_DEPLOYED_BYTECODE_GENERATED_SOURCES = "evm.deployedBytecode.generatedSources"
    """Sources generated by the compiler"""
    EVM_DEPLOYED_BYTECODE_IMMUTABLE_REFERENCES = (
        "evm.deployedBytecode.immutableReferences"
    )
    """Map from AST ids to bytecode ranges that reference immutables"""
    EVM_METHOD_IDENTIFIERS = "evm.methodIdentifiers"
    """The list of function hashes"""
    EVM_GAS_ESTIMATES = "evm.gasEstimates"
    """Function gas estimates"""
    EWASM_ALL = "ewasm"
    """All EWASM subassets"""
    EWASM_WAST = "ewasm.wast"
    """Ewasm in WebAssembly S-expressions format"""
    EWASM_WASM = "ewasm.wasm"
    """Ewasm in WebAssembly binary format"""
    ALL = "*"
    """All solc outputs including AST"""


class ModelCheckerEngineEnum(StrEnum):
    ALL = "all"
    BMC = "bmc"
    CHC = "chc"
    NONE = "none"


class ModelCheckerInvariantsEnum(StrEnum):
    CONTRACT = "contract"
    REENTRANCY = "reentrancy"


class ModelCheckerSolversEnum(StrEnum):
    CVC4 = "cvc4"
    SMTLIB2 = "smtlib2"
    Z3 = "z3"


class ModelCheckerTargetsEnum(StrEnum):
    CONSTANT_CONDITION = "constantCondition"
    UNDERFLOW = "underflow"
    OVERFLOW = "overflow"
    DIV_BY_ZERO = "divByZero"
    BALANCE = "balance"
    ASSERT = "assert"
    POP_EMPTY_ARRAY = "popEmptyArray"
    OUT_OF_BOUNDS = "outOfBounds"


def _to_camel(s: str) -> str:
    split = s.split("_")
    return split[0].lower() + "".join([w.capitalize() for w in split[1:]])


class SolcInputModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=_to_camel,
        populate_by_name=True,
        extra="allow",
        protected_namespaces=(),
    )


class SolcInputSource(SolcInputModel):
    keccak256: Optional[str] = None
    content: Optional[str] = None
    urls: Optional[List[str]] = None

    @model_validator(mode="before")
    def content_or_urls_set(cls, values):
        content, urls = values.get("content"), values.get("urls")
        assert (content is None) != (
            urls is None
        ), "SolcInputSource: exactly one of `content`, `urls` must be set"
        return values


class SolcInputOptimizerYulDetailsSettings(SolcInputModel):
    stack_allocation: Optional[bool] = None
    optimizer_steps: Optional[str] = None


class SolcInputOptimizerDetailsSettings(SolcInputModel):
    peephole: Optional[bool] = None
    inliner: Optional[bool] = None
    jumpdest_remover: Optional[bool] = None
    order_literals: Optional[bool] = None
    deduplicate: Optional[bool] = None
    cse: Optional[bool] = None
    constant_optimizer: Optional[bool] = None
    simple_counter_for_loop_unchecked_increment: Optional[bool] = None
    yul: Optional[bool] = None
    yul_details: Optional[SolcInputOptimizerYulDetailsSettings] = None


class SolcInputOptimizerSettings(SolcInputModel):
    enabled: Optional[bool] = None
    runs: Optional[int] = None
    details: Optional[SolcInputOptimizerDetailsSettings] = None


class SolcInputDebugRevertStringsSettingsEnum(StrEnum):
    """How to treat revert (and require) reason strings."""

    DEFAULT = "default"
    """Do not inject compiler-generated revert strings and keep user-supplied ones."""
    STRIP = "strip"
    """Remove all revert strings (if possible, i.e. if literals are used) keeping side-effects"""
    DEBUG = "debug"
    """Inject strings for compiler-generated internal reverts, implemented for ABI encoders V1 and V2 for now."""
    VERBOSE_DEBUG = "verboseDebug"
    """Even append further information to user-supplied revert strings (not yet implemented)"""


class SolcInputDebugInfoSettingsEnum(StrEnum):
    """How much extra debug information to include in comments in the produced EVM assembly and Yul code."""

    LOCATION = "location"
    """
    Annotations of the form `@src <index>:<start>:<end>` indicating the location of the corresponding element in the original Solidity file, where:
    * `<index>` is the file index matching the `@use-src` annotation,
    * `<start>` is the index of the first byte at that location,
    * `<end>` is the index of the first byte after that location.
    """
    SNIPPET = "snippet"
    """A single-line code snippet from the location indicated by `@src`. The snippet is quoted and follows the corresponding `@src` annotation."""


class SolcInputDebugSettings(SolcInputModel):
    revert_strings: Optional[SolcInputDebugRevertStringsSettingsEnum] = None
    debug_info: Optional[List[SolcInputDebugInfoSettingsEnum]] = None


class SolcInputMetadataSettings(SolcInputModel):
    append_CBOR: Optional[bool] = Field(None, alias="appendCBOR")
    use_literal_content: Optional[bool] = None
    bytecode_hash: Optional[MetadataBytecodeHashEnum] = None


class SolcInputModelCheckerSettings(SolcInputModel):
    contracts: Dict[str, List[str]] = {}  # source unit name -> list of contract names
    div_mod_with_slacks: Optional[bool] = None
    engine: Optional[ModelCheckerEngineEnum] = None
    invariants: List[ModelCheckerInvariantsEnum] = []
    show_unproved: Optional[bool] = None
    solvers: List[ModelCheckerSolversEnum] = []
    targets: List[ModelCheckerTargetsEnum] = []
    timeout: Optional[int] = None


class SolcInputSettings(SolcInputModel):
    stop_after: Optional[SolcStopAfterEnum] = None
    remappings: Optional[List[str]] = None
    optimizer: Optional[SolcInputOptimizerSettings] = None
    evm_version: Optional[EvmVersionEnum] = None
    via_IR: Optional[bool] = Field(None, alias="viaIR")
    debug: Optional[SolcInputDebugSettings] = None
    metadata: Optional[SolcInputMetadataSettings] = None
    libraries: Optional[
        Dict[str, Dict[str, str]]
    ] = None  # source unit name -> (lib name -> address)
    output_selection: Optional[
        Dict[str, Dict[str, List[SolcOutputSelectionEnum]]]
    ] = None  # source unit name -> (contract name / empty for whole file / start for all contracts ->
    model_checker: Optional[SolcInputModelCheckerSettings] = None


class SolcInput(SolcInputModel):
    language: SolcInputLanguageEnum = Field(SolcInputLanguageEnum.SOLIDITY)
    sources: Dict[str, SolcInputSource] = {}
    settings: Optional[SolcInputSettings] = None
