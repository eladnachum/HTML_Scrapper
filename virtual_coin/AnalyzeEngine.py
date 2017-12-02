class AnalayzeEngine(object):

    # A dict for storing each sequence pattern. key is the pattern. value is the prediction (up/down/can't determine)
    patterns = {}
    sequence_size = 7
    # range groups  0 , 1, 2, 3,4,5,6,7,8
    range_groups = [-5,-3,-2,-1,0,1,3,5,7,11]

    # def init_range_groups(self):
    #     for k,v in self.range_groups:
    #         key = "_"+k
    #         value = 0 - v
    #         self.range_groups[key]= value

    def __init__(self,data):
        self.data=data
        self.init_patterns()

    # check what group the param change belongs to
    def check_group(self,change):
        start_index = 0
        end_index = len(self.range_groups)-1
        if (change>=self.range_groups[end_index]): return end_index
        if (change<=self.range_groups[start_index]): return start_index

        while (start_index+1<end_index):
            index = start_index + ((end_index - start_index) / 2)
            if change == self.range_groups[index]: return index
            if change < self.range_groups[index]:
                end_index = index
            else:
                start_index = index

        return start_index

    def calculate_seq_pattern(self,seq_start_index,seq_end_index):
        pattern = ""
        for index in range(seq_start_index,seq_end_index):
            pattern = pattern + str(self.check_group(self.data[index].change))
        return pattern

    def init_patterns(self):
        for seq_start in range (1,len(self.data)-self.sequence_size):
            seq_end = seq_start+self.sequence_size
            pattern = self.calculate_seq_pattern(seq_start,seq_end)
            if pattern not in self.patterns:
                self.patterns[pattern] =  [self.data[seq_start-1].change,]
            else:
                self.patterns[pattern].append(self.data[seq_start-1].change)



    def forecast(self,index):
        last_seq_pattern = self.calculate_seq_pattern(index-self.sequence_size,index)
        return self.patterns[last_seq_pattern]
