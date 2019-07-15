class ParamTipo(object):

    def __init__(self, tipo, passagem):
        self.tipo = tipo
        self.passagem = passagem

    def getTipo(self):
        return self.tipo

    def getPassagem(self):
        return self.passagem

    def setTipo(self, tipo):
        self.tipo = tipo

    def setPassagem(self, passagem):
        self.passagem = passagem


class ForPar(object):

    def __init__(self, name, tipo, level, passagem):
        self.name = name
        self.category = "parametro formal"
        self.nivel = level
        self.tipo = tipo
        self.desloc = None
        self.passagem = passagem

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getNivel(self):
        return self.nivel

    def getTipo(self):
        return self.tipo

    def getDesloc(self):
        return self.desloc

    def getPassagem(self):
        return self.passagem

    def setNivel(self, nivel):
        self.nivel = nivel

    def setTipo(self, tipo):
        self.tipo = tipo

    def setDesloc(self, desloc):
        self.desloc = desloc

    def setPassagem(self, passagem):
        self.passagem = passagem


class SimVar(object):

    def __init__(self, name, tipo, nivel, desloc):
        self.name = name
        self.category = "variavel simples"
        self.nivel = nivel
        self.tipo = tipo
        self.desloc = desloc

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getNivel(self):
        return self.nivel

    def getTipo(self):
        return self.tipo

    def getDesloc(self):
        return self.desloc

    def setNivel(self, nivel):
        self.nivel = nivel

    def setTipo(self, tipo):
        self.tipo = tipo

    def setDesloc(self, desloc):
        self.desloc = desloc


class ProcDef(object):

    def __init__(self, name, nivel, nparam, param_list):
        self.name = name
        self.category = "procedure"
        self.nivel = nivel
        self.rotulo = None
        self.nparam = nparam
        self.param_list = param_list
        self.Symtab = []

    def setName(self, name):
        self.name = name

    def setCategory(self, category):
        self.category = category

    def setNivel(self, nivel):
        self.nivel = nivel

    def setRotulo(self, rotulo):
        self.rotulo = rotulo

    def addParam(self, tipo, passagem):
        ptipo = ParamTipo(tipo, passagem)
        for index, item in enumerate(self.param_list):
            if item is None:
                self.param_list[index] = ptipo
                break

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getNparam(self):
        return self.nparam

    def getNivel(self):
        return self.nivel

    def getRotulo(self):
        return self.rotulo

    def getParList(self):
        return self.param_list

    def setSymtab(self, Symtab):
        self.Symtab = Symtab

    def getSymtab(self):
        return self.Symtab


class FuncDef(object):

    def __init__(self, name, tipo, nivel, nparam, param_list):
        self.name = name
        self.category = "function"
        self.nivel = nivel
        self.rotulo = None
        self.nparam = nparam
        self.param_list = param_list
        self.return_type = tipo
        self.Symtab = None

    def setName(self, name):
        self.name = name

    def setCategory(self, category):
        self.category = category

    def setNivel(self, nivel):
        self.nivel = nivel

    def setRotulo(self, rotulo):
        self.rotulo = rotulo

    def addParam(self, tipo, passagem):
        ptipo = ParamTipo(tipo, passagem)
        for index, item in enumerate(self.param_list):
            if item is None:
                self.param_list[index] = ptipo
                break

    def setReturnType(self, tipo):
        self.return_type = tipo

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getNivel(self):
        return self.nivel

    def getNparam(self):
        return self.nparam

    def getRotulo(self):
        return self.rotulo

    def getReturnType(self):
        return self.return_type

    def getParList(self):
        return self.param_list

    def setSymtab(self, Symtab):
        self.Symtab = Symtab

    def getSymtab(self):
        return self.Symtab


class Token(object):    # The token class
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category
