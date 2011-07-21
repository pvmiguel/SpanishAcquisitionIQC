from pyparsing import (alphanums, alphas, delimitedList, nums, CaselessLiteral, Combine,
		Forward, Keyword, LineEnd, Literal, OneOrMore, Optional, ParserElement, QuotedString,
		SkipTo, StringEnd, Suppress, Word, ZeroOrMore)

from ..units import Quantity
from .tree import (Acquire, Assignment, Attribute, Block, Declaration, Delay, Dictionary,
		DictionaryItem, Loop, ParallelPulses, Pulse, PulseSequence, Variable)

"""
A parser for pulse programs.
"""


def Parser():
	old_whitespace = ParserElement.DEFAULT_WHITE_CHARS

	try:
		# Handle line breaks manually.
		ParserElement.setDefaultWhitespaceChars(ParserElement.DEFAULT_WHITE_CHARS.replace('\n', ''))

		# Keywords.
		## Types.
		DELAY, INT, OUTPUT, PULSE = Keyword('delay'), Keyword('int'), Keyword('output'), Keyword('pulse')

		## Syntax.
		ACQUIRE = Keyword('acquire').suppress()
		TERMINATOR = (LineEnd() | ';').suppress()
		TIMES = Keyword('times').suppress()

		# Values.
		identifier = Word(alphas + '_', alphanums + '_')

		## Numbers.
		### Integer.
		inum = Word('+-' + nums, nums).setParseAction(lambda x: int(x[0]))

		### Floating point.
		dot = Literal('.')
		e = CaselessLiteral('e')

		fractional_part = dot + Word(nums, nums)
		exponent_part = e + inum

		fnum = Combine(inum + (fractional_part + Optional(exponent_part) | exponent_part))
		fnum.setParseAction(lambda x: float(x[0]))

		number = fnum | inum

		## Quantities.
		# Unit symbol cannot start with "e".
		unit_symbol = Combine(Word(alphas.replace('E', '').replace('e', ''), alphas) + Optional(Word(nums)))
		unit_symbols = delimitedList(unit_symbol, delim='.', combine=True)
		quantity = (number + unit_symbols).setParseAction(lambda x: Quantity(x[0], x[1]))

		## Strings.
		string = QuotedString(r'"', escChar=r'\\') | QuotedString(r"'", escChar=r'\\')

		value = quantity | number | string

		## Dictionaries.
		dictionary_item = (identifier('key') + Suppress(':') + value('value')).setParseAction(DictionaryItem)
		dictionary = Suppress('{') + Optional(delimitedList(dictionary_item)) + Suppress('}')
		dictionary.setParseAction(Dictionary)

		# Variables.
		type = DELAY | INT | OUTPUT | PULSE

		attribute = (identifier('variable') + Suppress('.') + identifier('name')).setParseAction(Attribute)

		identifier_assignment = identifier('target') + Suppress('=') + (dictionary | identifier | value)('value')
		attribute_assignment = attribute('target') + Suppress('=') + (attribute | value)('value')
		assignment = (identifier_assignment | attribute_assignment).setParseAction(Assignment)

		declaration_list = delimitedList(assignment | identifier('name').setParseAction(Variable))
		declaration = (type('type') + declaration_list('variables')).setParseAction(Declaration)

		# Commands.
		## Acquire.
		acquire = ACQUIRE.setParseAction(Acquire)

		## Delay.
		delay = (quantity | identifier)('length').setParseAction(Delay)

		## Pulse.
		pulse_sequence = (Suppress('(') + OneOrMore(identifier | delay) + Suppress(')')) | identifier
		pulse_sequence.setParseAction(PulseSequence)
		pulse = (pulse_sequence('sequence') + Suppress(':') + identifier('target')).setParseAction(Pulse)
		pulses = OneOrMore(pulse).setParseAction(ParallelPulses)

		command = acquire | pulses | delay

		# Blocks.
		block = Forward().setParseAction(Block)
		loop_block = (TIMES + (identifier | inum)('times') + block('block')).setParseAction(Loop)

		# Statements.
		statement = Optional(assignment | declaration | command)
		# The last statement does not require a terminator.
		statements = ZeroOrMore(loop_block | statement + TERMINATOR) + statement

		block << (Suppress('{') + statements + Suppress('}'))

		parser = statements + StringEnd()

		# Comments.
		comment = Literal('#') + SkipTo(LineEnd())
		parser.ignore(comment)

		def parseString(s):
			return parser.parseString(s).asList()

		return parseString
	finally:
		ParserElement.setDefaultWhitespaceChars(old_whitespace)