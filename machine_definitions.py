from automathon import NFA
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

s = ''
s+='|------------------------------------------------------------------------|\n'
s+='|                                 Legend                                 |\n'
s+='|F: File (a|b|c|d|e|f|g|h) r: Rank (1|2|3|4|5|6|7|8) P: Piece (R|Q|N|B|K)|\n'
s+='|x: Capture (x)            +: Check (+)              #: Mate (#)         |\n'
s+='|------------------------------------------------------------------------|\n'

#univeral to all machines
piece    = 'P'
file     = 'F'
capture  = 'x'
rank     = 'r'
check    = '+'
mate     = '#'
epsilon  = 'ε'
alphabet = {piece, file, capture, rank, check, mate, epsilon}

class M:
    def __init__(self):        
        self.q  = {'MOVE\nSTART'} #always states
        self.q0 = 'MOVE\nSTART'   #always states
        self.f  = {'check','mate'} #check and mate are always ending characters
        self.sigma = alphabet
        self.legend = s
        self.delta = dict()
        self.automata = None

    def add_states_to_q(self, lst : list):
        for qn in lst:
            self.q.add(qn)

    def update_transistions_to_delta(self, qn : str, transistions : dict): #transistions must be a dict of key:value is str:set
        if qn not in self.delta.keys():
            self.delta[qn] = transistions

        if qn in self.delta.keys():
            for k,v in transistions.items():
                    self.delta[qn][k] = v

    #pawn only moves
    def green_machine(self):
        self.add_states_to_q(['file','pawn\ndid\ncapture','rank','check','mate'])
        self.f.add('rank')
        self.update_transistions_to_delta('MOVE\nSTART'       , {file  : {'file'}})
        self.update_transistions_to_delta('file'              , {rank  : {'rank'} , capture : {'pawn\ndid\ncapture'}})
        self.update_transistions_to_delta('pawn\ndid\ncapture', {rank  : {'rank'}})
        self.update_transistions_to_delta('rank'              , {check : {'check'}, mate    : {'mate'}, epsilon : {'rank'}})
        self.update_transistions_to_delta('check'             , {epsilon : {'check'}})
        self.update_transistions_to_delta('mate'              , {epsilon : {'mate'}})
        

    #identical to pawn only moves, but with a piece
    def light_green_machine(self):
        self.green_machine()
        self.add_states_to_q(['piece', 'piece\nstart.\nfile', 'piece\ndid\ncapture'    , 'piece\nending\nfile'])
        self.update_transistions_to_delta('MOVE\nSTART'         , {piece : {'piece'}})
        self.update_transistions_to_delta('piece'               , {file  : {'piece\nstart.\nfile'}, capture : {'piece\ndid\ncapture'}})
        self.update_transistions_to_delta('piece\ndid\ncapture' , {file  : {'piece\nending\nfile'}})
        self.update_transistions_to_delta('piece\nstart.\nfile' , {rank  : {'rank'}})
        self.update_transistions_to_delta('piece\nending\nfile' , {rank  : {'rank'}})

    #file disambiguated piece moves (math terms: two files, one rank)
    def yellow_machine(self):
        self.light_green_machine()
        self.update_transistions_to_delta('piece\nstart.\nfile' , {file  : {'piece\nending\nfile'}, capture : {'piece\ndid\ncapture'}, rank  : {'rank'}})

    #rank disambiguated piece moves (math terms: one file, two ranks)
    def red_machine(self):
        self.yellow_machine()
        self.add_states_to_q(['piece\nstart.\nrank'])
        self.update_transistions_to_delta('piece'         , {rank : {'piece\nstart.\nrank'}, file  : {'piece\nstart.\nfile'}, capture : {'piece\ndid\ncapture'}})
        self.update_transistions_to_delta('piece\nstart.\nrank' , {file  : {'piece\nstart.\nfile'}, capture : {'piece\ndid\ncapture'}})

    #doubly disambiguated piece moves (math terms: two files, two ranks)
    def dark_red_machine(self):
        self.red_machine()
        self.add_states_to_q(['rank\ndisamb.'])
        self.update_transistions_to_delta('piece\nstart.\nfile' , {file  : {'piece\nending\nfile'}, capture : {'piece\ndid\ncapture'}, rank  : {'rank', 'rank\ndisamb.'}})
        self.update_transistions_to_delta('rank\ndisamb.'       , {file  : {'piece\nending\nfile'}, capture : {'piece\ndid\ncapture'}})

    def stamp_legend(self, name = 'automata'):
        image = Image.open(f'{name}.gv.png')
        # image = ImageOps.expand(image, border = 120, fill = (255,255,255))
        image = ImageOps.invert(image.convert('RGB'))
        draw  = ImageDraw.Draw(image)
        text  = self.legend
        font  = ImageFont.truetype('consola.ttf', 28)
        pos   = (720,20)
        color = "rgb(255,0,127)"  # White color
        draw.text(pos, text, fill=color, font=font)
        image.save(f'{name}.gv.png')

    def process_automata(self, name='automata'):
        automata = NFA(self.q, self.sigma, self.delta, self.q0, self.f)
        filename = name
        automata.view(
            file_name=name,
            node_attr={'fontsize': '25'},
            edge_attr={'fontsize': '25pt'}
        )
        print(f"Validity: {automata.is_valid()}")
        moves = ['Fr','Fr+','Fr#','Fxr','Fxr+','Fxr#','PFr','PFr+','PFr#','PxFr','PxFr+','PxFr#','PFFr','PFFr+','PFFr#','PFxFr','PFxFr+','PFxFr#','PrFr','PrFr+','PrFr#','PrxFr','PrxFr+','PrxFr#','PFrFr','PFrFr+','PFrFr#','PFrxFr','PFrxFr+','PFrxFr#']
        fi = open('missing_moves.txt','w')
        mvs = ''
        for move in moves:
            if automata.accept(move) == False:
                mvs += f'{move} '
                fi.write(f'{move}\n')
        print("Rejected: ", mvs)
        fi.close()
        self.automata = automata
        # self.stamp_legend(name=name)
