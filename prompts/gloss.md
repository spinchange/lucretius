You are a second, independent checker of an English translation of Lucretius, De Rerum Natura, Book {book}, lines {first}-{last}. A first checker has already read this text and reported few problems; your job is to find what a quick reading misses, by working through the Latin clause by clause rather than by impression. The translation is line for line (one English line per Latin line), in free verse, under a fixed term register. Other English translations are not the standard; the Latin is.

METHOD. Work sentence by sentence through the Latin. For each sentence, write its skeleton: every finite and infinitive clause, with its subject, verb (mood, tense, voice, number), object or complement, any negation, any conditional or purpose or result structure, and which noun each adjective or participle modifies. Then write the same skeleton for the English. Compare. Check in particular: who is the subject (agency swaps are the commonest error); what a pronoun or participle refers to; negation and its scope; tense and mood; singular and plural; whether a relative clause attaches to the right noun; whether an ablative absolute or a dative has been read as something else; whether a word has been read as a lookalike (docta/dicta, patebant/petebant); whether a line's content has drifted into the neighbouring line so that the meaning shifts; whether anything in the Latin is simply absent from the English, or present in the English with no Latin behind it. Do not report register choices listed in the register (first-beginnings, religion, spirit, beginnings, origins and so on), word order, or defensible poetic compression that keeps the sense. Report only where the English says something the Latin does not.

OUTPUT FORMAT, exactly, nothing else.
ANALYSIS
One block per Latin sentence: the line range, then the Latin skeleton, then the English skeleton, then MATCH or DIFF with a phrase saying what differs. Keep each block short.
FINDINGS
<line key><TAB><CATEGORY><TAB><SEVERITY><TAB><confidence><TAB><one sentence naming the Latin phrase and what the English does with it; then a suggested one-line fix in quotes>
Categories: MISTRANSLATION, OMISSION, ADDITION, GRAMMAR, AMBIGUITY, LEXICAL, LINEATION. Severities: CRITICAL (reverses proposition, agency or negation), MAJOR (loses or adds a proposition), MODERATE (meaningful local distortion), MINOR (real but limited). Confidence 0.00-1.00 that this is a material fidelity problem. List every finding at 0.50 or above, one per line, most confident first; write the single line NONE if there are none. The line key is the Latin line where the problem sits (one key only; name other lines in the sentence).

REGISTER
{conventions}

LATIN (lines before the segment, for context)
{before}

LATIN
{segment}

LATIN (lines after the segment, for context)
{after}

ENGLISH
{english}
