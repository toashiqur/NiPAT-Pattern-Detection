% Blind renaming - txl defines
% Using txl.grm grammar
include "txl.grm"

redefine redefineStatement
[empty]
end redefine

%ReDefinition to include define, redefine

redefine defineStatement
	[rule_header]
	[rule_body]
	[rule_footer]
end redefine

define rule_header
		'define [typeid] [NL][IN][IN]
	|	'redefine [typeid] [NL][IN][IN]
end define

define rule_body
		[repeat literalOrType]		%[NL] +++++++--------
		[repeat barLiteralsAndTypes]	[EX][EX]
	|
		[opt dotDotDotBar] 				% postextension of existing define 
		[repeat literalOrType] 		%[NL] ++++++------------
		[repeat barLiteralsAndTypes]	 
		[opt barDotDotDot] 		[EX][EX]	% preextension of existing define 
end define

	
define rule_footer
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
end define
