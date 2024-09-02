import random


class Skin:
    def __init__(self, name, rarity, collection, min_float, max_float):
        self.skin_name = name
        self.rarity = rarity
        self.collection = collection
        self.min_float = min_float
        self.max_float = max_float
        self.yield_percentage = None
        self.__outcome_float = None
        self.outcome_quality = None

    def __str__(self):
        return "---------------------------" + "\n" + self.skin_name + "\n" + "Rarity: " + self.rarity + "\n" + \
               "Collection: " + self.collection + "\n" + "Min Float: " + str(self.min_float) + "\n" \
               + "Max Float: " + str(self.max_float) + "\n" + "---------------------------"

    def SetOutcomeFloat(self, outcome_float):
        self.__outcome_float = outcome_float
        if self.__outcome_float >= 0.44:
            self.outcome_quality = "Battle-Scarred"
        elif self.__outcome_float >= 0.37:
            self.outcome_quality = "Well-Worn"
        elif self.__outcome_float >= 0.15:
            self.outcome_quality = "Field-Tested"
        elif self.__outcome_float >= 0.07:
            self.outcome_quality = "Minimal Wear"
        else:
            self.outcome_quality = "Factory New"

    def GetOutcomeFloat(self):
        return self.__outcome_float

class TradeUpCalculator:
    def __init__(self, skins):
        self.input_skins = skins

    def CalculateAverageFloat(self):
        self.sum = 0
        for item in self.input_skins:
            self.sum += (item.min_float + item.max_float) / 2  # CHANGE THIS LATER
            print(item)

        self.average_float = self.sum / len(self.input_skins)

        return self.average_float

    def CalculateOutcomeProbabilities(self, all_skins, average_float):
        self.all_skins = all_skins
        self.average_float = average_float
        self.outcome_skins = []
        for input_skin in self.input_skins:
            for skin in all_skins:  # Make more efficient by just searching through the correct rarity list
                if skin.rarity == self.UpRarity(input_skin.rarity) and skin.collection == input_skin.collection:
                    self.outcome_skins.append(skin)

        for skin in self.outcome_skins:  # Set the skin's yield percentages
            freq = self.outcome_skins.count(skin)
            skin.yield_percentage = float(freq) / len(self.outcome_skins)

        self.cleaned_output_skins = ["test"]
        i = 0
        for skin in self.outcome_skins:  # Clean up the list
            if len(self.cleaned_output_skins) == 1 and i == 0:
                self.cleaned_output_skins[0] = skin
            if skin not in self.cleaned_output_skins:
                self.cleaned_output_skins.append(skin)
            i += 1

        print("Length of list is " + str(len(self.cleaned_output_skins)))

        for skin in self.cleaned_output_skins:  # Print the list and set their outcome floats
            skin.SetOutcomeFloat(((skin.max_float - skin.min_float) * self.average_float) + skin.min_float)
            print(skin.skin_name + f" {skin.yield_percentage:.2%}" + " with a quality " + str(skin.outcome_quality) + " and float of " + str(skin.GetOutcomeFloat()))

    def UpRarity(self, rarity):
        if rarity == Constants.CONSUMER_GRADE:
            return Constants.INDUSTRIAL_GRADE
        elif rarity == Constants.INDUSTRIAL_GRADE:
            return Constants.MIL_SPEC
        elif rarity == Constants.MIL_SPEC:
            return Constants.RESTRICTED
        elif rarity == Constants.RESTRICTED:
            return Constants.CLASSIFIED
        else:
            return


class TradeUpManager:
    def __init__(self, all_skins):
        self.all_skins = all_skins
        self.input_skins = []
        self.contract_input_rarity = None
        self.consumer_grade = []
        self.industrial_grade = []
        self.mil_spec = []
        self.restricted = []
        self.classified = []
        self.input_skins_rarity_list = []

    def CreateRandomInputSkins(self):
        self.CreateRandomTradeUpRarity()
        self.SortSkins()
        for x in range(10):
            self.input_skins.append(self.input_skins_rarity_list[random.randint(0, len(self.input_skins_rarity_list))])

        return self.input_skins

    def CreateRandomTradeUpRarity(self):
        i = random.randint(0, 3)
        if i == 0:
            self.contract_input_rarity = Constants.CONSUMER_GRADE
            self.input_skins_rarity_list = self.consumer_grade
        elif i == 1:
            self.contract_input_rarity = Constants.INDUSTRIAL_GRADE
            self.input_skins_rarity_list = self.industrial_grade
        elif i == 2:
            self.contract_input_rarity = Constants.MIL_SPEC
            self.input_skins_rarity_list = self.mil_spec
        else:
            self.contract_input_rarity = Constants.RESTRICTED
            self.input_skins_rarity_list = self.restricted
        # If including a classified tradeup into extraordinary, then put that here.

    def SortSkins(self):
        for item in self.all_skins:
            if item.rarity == Constants.CONSUMER_GRADE:
                self.consumer_grade.append(item)
            elif item.rarity == Constants.INDUSTRIAL_GRADE:
                self.industrial_grade.append(item)
            elif item.rarity == Constants.MIL_SPEC:
                self.mil_spec.append(item)
            elif item.rarity == Constants.RESTRICTED:
                self.restricted.append(item)
            elif item.rarity == Constants.CLASSIFIED:
                self.classified.append(item)


class Constants:  # Makeshift enum
    CONSUMER_GRADE = "Consumer Grade"
    INDUSTRIAL_GRADE = "Industrial Grade"
    MIL_SPEC = "Mil-Spec Grade"
    RESTRICTED = "Restricted"
    CLASSIFIED = "Classified"
