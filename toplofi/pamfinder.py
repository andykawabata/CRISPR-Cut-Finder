import math

def get_crispr_info(base_pair):
    with open('sequence.txt') as f:
        def go_to_position_return_rest_of_line(position):
            if position % 70 != 0:
                lines_to_skip = math.floor(position/70)
                remainder = position % 70
                for i in range(lines_to_skip):
                    next(f)
                line = f.readline()
                base_position = remainder - 1  # account for my chr11 file being off by 1
                part_of_line = line[base_position:]
                return part_of_line
            else:
                linestoskip = math.floor(position/70) - 1
                for i in range(linestoskip):
                    next(f)
                line = f.readline()
                return line[69]
        def create_string_with_target_position_at_200(target_position):
            position = target_position - 200
            new_string = go_to_position_return_rest_of_line(position)
            for i in range(7):
                new_string += f.readline()
            return new_string.replace('\n', '')
        def find_guide(i, type,seq):
            if type == 'G':
                if i-22 >= 0:
                    return seq[i-21:i-1]
                else:
                    return -1
            if type == 'C':
                if i+22 < len(seq):
                    pre_str = seq[i+3:i+23]
                    new_str = take_compliment(pre_str)
                    return new_str
                else:
                    return -1
        def reverse_and_compliment(seq):
            new_str = ''
            for i in range(len(seq)-1, -1, -1):
                letter = seq[i]
                if letter == 'A':
                    new_str += 'T'
                if letter == 'C':
                    new_str += 'G'
                if letter == 'G':
                    new_str += 'C'
                if letter == 'T':
                    new_str += 'A'
            return new_str

        def take_compliment(seq):
            new_str = ''
            for i in range(0, len(seq)):
                letter = seq[i]
                if letter == 'A':
                    new_str += 'T'
                if letter == 'C':
                    new_str += 'G'
                if letter == 'G':
                    new_str += 'C'
                if letter == 'T':
                    new_str += 'A'
                if letter == '/':
                    new_str += '\\'
                if letter == '\\':
                    new_str += '/'
                if letter == '|':
                    new_str += '|'
            return new_str
        def index_and_type_of_first_cut(seq):
                for i in range(195, len(seq)):
                    if seq[i] == 'G' and seq[i+1] == 'G':
                        if i >= 205:
                            guide = find_guide(i, 'G', seq)
                            return [i, 'G', guide]
                    if seq[i] == 'C' and seq[i+1] == 'C':
                        better_cut = find_GG(i+2, seq)
                        if better_cut == -1:
                            guide = find_guide(i, 'C', seq)
                            return [i, 'C', guide]
                        else:
                            guide = find_guide(better_cut, 'G', seq)
                            return [better_cut, 'G', guide]
        def find_GG(index_after, seq):
                for i in range(0, 8):
                    if seq[index_after+i] == 'G' and seq[index_after+i+1] == 'G':
                        if i >= 205:
                            return index_after + i
                return -1
        def base_to_left_of_cut(cut_info):
                if cut_info[1] == 'C':
                    return cut_info[0] + 5
                if cut_info[1] == 'G':
                    return cut_info[0] - 5
        def index_and_type_of_second_cut(seq, first_cut):#first_cut = base to left of first cut
                for i in range(205, 0, -1):
                    if seq[i] == 'C' and seq[i-1] == 'C':
                        if i <= 195 and i + 21 <= first_cut: #make sure the guide rna sequence isn't cut off
                            guide = find_guide(i-1, 'C', seq)
                            return[i-1, 'C', guide]
                    if seq[i] == 'G' and seq[i-1] == 'G':
                        if i <= first_cut:
                            better_cut = find_CC(i-2, seq, first_cut)
                            if better_cut == -1:
                                guide = find_guide(i - 1, 'G', seq)
                                return [i-1, 'G', guide]
                            else:
                                guide = find_guide(better_cut, 'C', seq)
                                return [better_cut, 'C', guide]
        def find_CC(index_before, seq, first_cut):
                for i in range(0, 8):
                    if seq[index_before-i] == 'C' and seq[index_before-i-1] == 'C':
                        if i <= 195 and i + 21 <= first_cut:
                            return index_before - i - 1
                return -1



        my_string = create_string_with_target_position_at_200(base_pair)
        pre_first_cut = index_and_type_of_first_cut(my_string)
        first_cut = base_to_left_of_cut(pre_first_cut)
        pre_second_cut = index_and_type_of_second_cut(my_string, first_cut)
        second_cut = base_to_left_of_cut(pre_second_cut)


        def add_symbols_and_cut_exccess(seq):
            if(second_cut >= 20 and first_cut <= len(seq) -20):
                new_str = seq[second_cut - 20:second_cut + 1] + \
                          '//' + \
                          seq[second_cut + 1:200] + \
                          '|' + \
                          seq[200] + \
                          '|' + \
                          seq[201:first_cut + 1] + \
                          '\\\\' + \
                          seq[first_cut + 1: first_cut+20]
                return new_str
            else:
                return "Cut was too far away from target"
        def find_guide__position_offset_from_target(pre_cut_info):
            start_off_set = 0
            if(pre_cut_info[1] == 'G'):
                end = pre_cut_info[0] - 2 - 200
                start_off_set = end - 19
            if(pre_cut_info[1] == 'C'):
                start_off_set = pre_cut_info[0] - 200 + 3
            return start_off_set
        def splice_sequence(seq):
            a = seq.find('/')
            b = seq.find('|')
            c = seq.find('\\')
            new_str = seq[a+2:b] + seq[b+1] + seq[b+3:c]
            new_str_compliment = take_compliment(new_str)
            return (new_str, new_str_compliment)





        def ref_offset(seq):
            return seq.find('|') + 1



        top_seq_with_symbols = add_symbols_and_cut_exccess(my_string)
        bottom_seq_with_symbols = take_compliment(top_seq_with_symbols)
        offset_first_cut = find_guide__position_offset_from_target(pre_first_cut)
        first_guide = pre_first_cut[2]
        offset_second_cut = find_guide__position_offset_from_target(pre_second_cut)
        second_guide = pre_second_cut[2]
        ref_string = ref_offset(top_seq_with_symbols)
        splice_sequence = splice_sequence(top_seq_with_symbols)
        splice_length = len(splice_sequence[0])
        print(pre_first_cut[0])
        return top_seq_with_symbols, bottom_seq_with_symbols, first_guide, offset_first_cut, second_guide, \
               offset_second_cut, ref_string, splice_length, splice_sequence

print(get_crispr_info(100000))