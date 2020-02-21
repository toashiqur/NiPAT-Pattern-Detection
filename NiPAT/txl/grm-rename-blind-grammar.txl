include "txl.grm"
include "bom.grm"

%Redefine in DefineStatement

redefine redefineStatement
[empty]
end redefine

%ReDefinition to include rule, function, define, redefine, replace, match

redefine defineStatement
	[defineHeader] [NL] [IN]
	[defineBody]
	[defineFooter]
end redefine


define defineHeader
		'define [typeid]
	|	'redefine [typeid]
end define

define defineBody
		[repeat literalOrType]		[NL] 
		[repeat barLiteralsAndTypes]	[EX][EX] 
	|
		[opt dotDotDotBar] 				% postextension of existing define 
		[repeat literalOrType] 		[NL] 
		[repeat barLiteralsAndTypes]	 
		[opt barDotDotDot] 		[EX][EX]	% preextension of existing define 
end define
	
define defineFooter
		'end 'define 
		[RESET]
	|	'end 'redefine
		[RESET]
end define


define potential_clone
    [defineStatement]
end define
include "generic-rename-blind.txl"

redefine end_xml_source_coordinate
    [NL] [SPOFF] '</ 'source '> [SPON] [NL]
end redefine
