############################################################################################################################
# FirstPredictions                                                                                                         #
# Used to rank teams and predict matches                                                                                   #                                                                                     #
############################################################################################################################

class MitchRating:
    def __init__(self, k, g = 1):
        self.k = k
        self.g = g