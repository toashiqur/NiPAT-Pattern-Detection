include "txl.grm"
include "bom.grm"

%Redefine in ruleStatement
redefine functionStatement
[empty]
end redefine

redefine defineStatement
[empty]
end redefine

redefine redefineStatement
[empty]
end redefine

redefine ruleStatement
[empty]
end redefine
%ReDefinition to include  define, redefine, rule, function, replace, match

define blockStatement
	[blockHeader] [NL] [IN] [IN]
	[blockBody]
	[blockFooter] [NL]
end define


define blockHeader
		'define [typeid]
	|	'redefine [typeid]
	|	'rule [ruleid] [repeat formalArgument]	
	| 	'function [ruleid] [repeat formalArgument]
end define

define blockBody		
		% This order is necessary-define must go after redefine
		% otherwise ... goes as part of repeat literal of define..
		
    	% redefine definition- [opt quote] added extra with the original- Moon
		[opt dotDotDotBar] 				% postextension of existing define 
		[opt quote] [repeat literalOrType] 	 
		[repeat barLiteralsAndTypes]
		[opt barDotDotDot] 	[EX][EX][EX]	% preextension of existing define 

    |   % define definition- [opt quote] added extra with original- Moon
		[opt quote] [repeat literalOrType]	 
		[repeat barLiteralsAndTypes] [EX] [EX]
		
	|	% rule/function original definition
		[repeat constructDeconstructImportExportOrCondition] 	[EX] [EX]
		[EX] [opt skippingType]
		[replace_match]		[EX]
end define

define replace_match
	'replace [opt dollarStar] [SP] [type]			[NL][IN] 
			[pattern]
		[repeat constructDeconstructImportExportOrCondition] 
		[EX] 'by						[NL][IN] 
			[replacement] 
	|
	'match [opt dollarStar] [SP] [type]			[NL][IN]
			[pattern] 
		[repeat constructDeconstructImportExportOrCondition]
end define
	
define blockFooter
		'end 'define
		[RESET]
	|	'end 'redefine
		[RESET]
	|	'end 'rule
	|	'end 'function	
end define

define quote
    ''
end define

define potentialClone
    [blockStatement]
end define

include "normalize-txl-blocks.rul"
