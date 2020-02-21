include "txl.grm"
include "bom.grm"

redefine defineStatement
[empty]
end redefine

redefine redefineStatement
[empty]
end redefine

redefine functionStatement
[empty]
end redefine

redefine ruleStatement
[empty]
end redefine

% Now include all in txlBlock definition...
define txlBlock
	[txlBlockHeader] [NL] [IN]
	[txlBlockBody]
	[txlBlockFooter]
end define


define txlBlockHeader
		'rule [ruleid] [repeat formalArgument]	
	| 	'function [ruleid] [repeat formalArgument]
	|	'define [typeid]
	|	'redefine [typeid]
end define

define txlBlockBody
		[repeat constructDeconstructImportExportOrCondition] 	
		[EX] [opt skippingType]
		[replace_match] [EX]
	|
		[repeat literalOrType]		[NL] 
		[repeat barLiteralsAndTypes]	[EX][EX] 
	|
		[opt dotDotDotBar] 				% postextension of existing define 
		[repeat literalOrType] 		[NL] 
		[repeat barLiteralsAndTypes]	 
		[opt barDotDotDot] 		[EX][EX]	% preextension of existing define 
end define

define replace_match
	'replace [opt dollarStar] [SP] [type]			[NL][IN] 
			[pattern]
		[repeat constructDeconstructImportExportOrCondition] 
		[EX] 'by						[NL][IN] 
			[replacement] 					[EX][EX]
	|
	'match [opt dollarStar] [SP] [type]			[NL][IN]
			[pattern] 
		[repeat constructDeconstructImportExportOrCondition] 
end define
	
define txlBlockFooter
		'end 'define 
		[RESET]
	|	'end 'redefine
		[RESET]
	|	'end 'rule		 
	|	'end 'function	
end define


define potential_clone
    [txlBlock]
end define
include "generic-rename-blind.txl"

redefine end_xml_source_coordinate
    [NL] [SPOFF] '</ 'source '> [SPON] [NL]
end redefine
