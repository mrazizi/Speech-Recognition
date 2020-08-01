import argparse
import wer

# create a function that calls wer.string_edit_distance() on every utterance
# and accumulates the errors for the corpus. Then, report the word error rate (WER)
# and the sentence error rate (SER). The WER should include the the total errors as well as the
# separately reporting the percentage of insertions, deletions and substitutions.
# The function signature is
# num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=reference_string, hyp=hypothesis_string)
#
def score(ref_trn=None, hyp_trn=None):

    # reading reference and hypothesis files
    with open(ref_trn) as ref_file:
        ref_lines = ref_file.readlines()
    with open(hyp_trn) as hyp_file:
        hyp_lines = hyp_file.readlines()

    # variables related to sentence error calculation
    n_sentences = len(ref_lines)
    n_incorrect_sentences = n_sentences

    # variables related to word error calculation
    n_ref_words = 0
    n_incorrect_words = 0
    n_sub_errors = 0
    n_ins_errors = 0
    n_del_errors = 0
    word_error_rate = 0
    sub_error_rate = 0
    ins_error_rate = 0
    del_error_rate = 0


    # iterating on all hyp sentences and finding the corresponding ref sentence
    for hyp_line in hyp_lines:
        open_p_index = hyp_line.find("(")
        close_p_index = hyp_line.find(")")
        hyp_root_name = hyp_line[open_p_index+1: close_p_index]
        hyp_sentence = hyp_line[: open_p_index-1].split(" ")
        # removing empty strings
        hyp_sentence = [x for x in hyp_sentence if x]

        for ref_line in ref_lines:
            open_p_index = ref_line.find("(")
            close_p_index = ref_line.find(")")
            ref_root_name = ref_line[open_p_index + 1: close_p_index]

            if hyp_root_name == ref_root_name:
                ref_sentence = ref_line[: open_p_index - 1].split(" ")
                # removing empty strings
                ref_sentence = [x for x in ref_sentence if x]

                num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=ref_sentence, hyp=hyp_sentence)

                # sentence error calculation
                if num_errors == 0:
                    n_incorrect_sentences -= 1

                # word error calculation
                n_ref_words += len(ref_sentence)
                n_incorrect_words += num_errors
                n_sub_errors += num_substitutions
                n_del_errors += num_deletions
                n_ins_errors += num_insertions

                # printing results
                print(f"id: ({hyp_root_name})")
                print(f"Scores: N={num_tokens}, S={num_substitutions}, D={num_deletions}, I={num_insertions}")
                print()
                break


    # calculating rates
    word_error_rate = (n_incorrect_words / n_ref_words) * 100
    sub_error_rate = (n_sub_errors / n_ref_words) * 100
    del_error_rate = (n_del_errors / n_ref_words) * 100
    ins_error_rate = (n_ins_errors / n_ref_words) * 100

    print("-----------------------------------")
    print("Sentence Error Rate:")
    print(f"Sum: N={n_sentences}, Err={n_incorrect_sentences}")
    print(f"Avg: N={n_sentences}, Err={(n_incorrect_sentences / n_sentences) * 100}%")
    print("-----------------------------------")
    print("Word Error Rate:")
    print(f"Sum: N={n_ref_words}, Err={n_incorrect_words}, Sub={n_sub_errors}, Del={n_del_errors}, Ins={n_ins_errors}")
    print(f"Avg: N={n_ref_words}, Err={word_error_rate:.2f}%, Sub={sub_error_rate:.2f}%, Del={del_error_rate:.2f}%, Ins={ins_error_rate:.2f}%")
    print("-----------------------------------")





    return


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
                                                 "Computes Word Error Rate and Sentence Error Rate")
    parser.add_argument('-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    parser.add_argument('-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    args = parser.parse_args()

    if args.reftrn is None or args.hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    score(ref_trn=args.reftrn, hyp_trn=args.hyptrn)
