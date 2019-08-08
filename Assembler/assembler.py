import json
import os
from os import listdir
from os.path import isfile, join
import time


class assembler:

    def __init__(self):
        pass

    def __RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def returnType(self, token):
        regCharacters = ["A", "B", "C", "D"]
        isAddress = False
        if token.startswith('[') and token.endswith(']'):
            isAddress = True
            token = token.replace("[", "")
            token = token.replace("]", "")

        if "," in token:
            token = token.replace(",", "")
        if self.RepresentsInt(token):
            if isAddress:
                return "[const]"
            else:
                return "const"
        elif len(token) == 1 and token in regCharacters:
            if isAddress:
                return "[reg]"
            else:
                return "reg"
        elif self.isALabel(token):
            if isAddress:
                return "[const]"
            else:
                return "const"

    def tokensToInstruc(self, tokens):
        instruc = ""
        if len(tokens) > 0:
            instruc = instruc + tokens[0]
        if len(tokens) > 1:
            instruc = instruc + "_" + self.returnType(tokens[1])
        if len(tokens) > 2:
            instruc = instruc + "_" + self.returnType(tokens[2])
        return instruc

    def getListOfLabels(self):
        self.listOfLabels = []
        labelContent = self.linesToAssemble
        for lx in range(0, len(labelContent)):
            labelTokens = str.split(labelContent[lx])
            if len(labelTokens) > 0:
                if str(labelTokens[0][-1:]) == ":":
                    self.listOfLabels.append(
                        labelTokens[0].replace(":", ""))
        return self.listOfLabels

    def getLabelNumbers(self):
        self.labelNumbers = []
        currentByte = 0
        labelContent = self.linesToAssemble
        for lx in range(0, len(labelContent)):

            labelTokens = str.split(labelContent[lx])
            if len(labelTokens) > 0:
                if str(labelTokens[0][-1:]) == ":":
                    self.labelNumbers.append(currentByte)
                elif self.instrucToBinary(self.tokensToInstruc(labelTokens)):
                    currentByte += len(labelTokens)
        return self.labelNumbers

    def isALabel(self, string):
        if string in self.listOfLabels:
            return True
        else:
            return False

    def instrucToBinary(self, string):
        with open(f"./instrucToBinary.json") as json_data:
            binInstruc = json.load(json_data)
            try:
                return binInstruc[string]
            except:
                return False

    def regToBinary(self, reg):
        reg = reg.replace(",", "")
        if reg == "A":
            return 0
        elif reg == "B":
            return 1
        elif reg == "C":
            return 2
        elif reg == "D":
            return 3
        else:
            return False

    def constToBinary(self, const):
        if const.startswith('[') and const.endswith(']'):
            const = const.replace("[", "")
            const = const.replace("]", "")
        if self.isALabel(const):
            return self.labelNumbers[self.listOfLabels.index(const)]
        else:
            return int(const.replace(",", ""))

    """
    takes list of file lines and returns a bytearray of corresponding machine code
    """
    def assemble(self, linesToAssemble):

        self.linesToAssemble = linesToAssemble
        self.content = linesToAssemble
        self.listOfLabels = self.getListOfLabels()
        self.labelNumbers = self.getLabelNumbers()
        self.machineCodeBytes = bytearray()

        for x in range(0, len(self.content)):
            tokens = str.split(self.content[x])
            instruc = self.tokensToInstruc(tokens)
            instructionBytes = []

            # if "tokens" represnt a valid instruction
            if self.instrucToBinary(self.tokensToInstruc(tokens)):
                self.machineCodeBytes.append(
                    int(self.instrucToBinary(self.tokensToInstruc(tokens))))
                if len(tokens) > 1:
                    if "reg" in self.returnType(tokens[1]):
                        self.machineCodeBytes.append(
                            self.regToBinary(tokens[1]))
                    elif "const" in self.returnType(tokens[1]):
                        self.machineCodeBytes.append(
                            self.constToBinary(tokens[1]))
                if len(tokens) > 2:
                    if "reg" in self.returnType(tokens[2]):
                        self.machineCodeBytes.append(
                            self.regToBinary(tokens[2]))
                    elif "const" in self.returnType(tokens[2]):
                        self.machineCodeBytes.append(
                            self.constToBinary(tokens[2]))

        return self.machineCodeBytes
