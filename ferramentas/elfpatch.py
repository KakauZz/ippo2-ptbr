import re
M={
'YES':'SIM','NO':'NAO','CANCEL':'CANCELAR','SAVE':'SALVAR','LOAD':'CARREGAR','NEW GAME':'NOVO JOGO','LOAD GAME':'CARREGAR JOGO',
'HEIGHT':'ALTURA','REACH':'ALCANCE','HAND':'MAO','WEIGHT':'PESO','STYLE':'ESTILO','WEIGHT CLASS':'CATEGORIA',
'SUN':'DOM','MON':'SEG','TUE':'TER','WED':'QUA','THU':'QUI','FRI':'SEX','SAT':'SAB',
'POWER':'FORCA','SPEED':'VELOC.','STAMINA':'FOLEGO','HOLIDAY':'FOLGA','DOCTOR':'DOUTOR','ON':'SIM','OFF':'NAO',
'WEIGHT COACH':'TREINO DE PESO','SLEEP':'DORMIR','SELECT MENU':'ESCOLHER','SETTING MENU':'CONFIGURAR','NUTRITION':'NUTRICAO',
'SPECIAL TRAINING':'TREINO ESPECIAL','NORMAL TRAINING':'TREINO NORMAL','BOXER MODE':'MODO BOXEADOR','SECOND MODE':'MODO TECNICO',
'AUDIENCE MODE':'MODO PLATEIA','CHARACTER TEMPLATE':'MODELO PRONTO','GENERATE TEMPLATE':'GERAR MODELO',
'LIFE':'VIDA','ENDURANCE':'RESISTENCIA','RUSH STAMINA':'FOLEGO RUSH','BAD HEALTH':'MA SAUDE','FATIGUE':'CANSACO',
'SPEED AVERAGE':'MEDIA VELOC.','HAND SP':'VEL. MAO','SWAY SP':'VEL. ESQUIVA','FOOTWORK SP':'VEL. PERNAS','DASH SP':'VEL. AVANCO',
'HEAVY PUNCH POW':'FORCA SOCO PESADO','SOLID PUNCH POW':'FORCA SOCO FIRME','GLUCOSE':'GLICOSE','AMINO ACID':'AMINOACIDOS',
'FATTY ACID':'ACIDOS GRAXOS','WATER':'AGUA','MINERAL':'MINERAIS','VITAMIN':'VITAMINAS','FAT':'GORDURA','BASAL METABOLISM':'METABOLISMO BASAL',
'STAMINA RATE':'TAXA DE FOLEGO','TWIST BODY':'GIRO DO CORPO','TECHNIC':'TECNICA','CONCENTRATION':'CONCENTRACAO',
'NECK MUSCLES':'PESCOCO','BACK MUSCLES':'COSTAS','CHEST MUSCLES':'PEITO','ABDOMEN MUSCLES':'ABDOMEN','BRACHIAL MUSCLES':'BICEPS',
'ARM MUSCLES':'BRACOS','HIP MUSCLES':'QUADRIL','THIGH MUSCLES':'COXAS','CALVES MUSCLES':'PANTURRILHA','CAREER':'CARREIRA',
'POW AVERAGE':'MEDIA FORCA','MUSCLES AVERAGE':'MEDIA MUSCULOS','BEARD':'BARBA','MUSTACHE':'BIGODE','BLOW':'GOLPE','STRATEGY':'ESTRATEGIA',
'TOURNAMENT':'TORNEIO','DECORATION BODY':'ACESSORIO CORPO','DECORATION HEAD':'ACESSORIO CABECA','BOXER ALL':'BOXEADOR',
'SHOES':'BOTAS','TRUNKS':'CALCAO','HAIR':'CABELO','BODY':'CORPO','FACE':'ROSTO','BOXROAD DATA':'DADOS CARREIRA','NO DATA':'SEM DADOS',
'REMATCH':'REVANCHE','REPLAY SAVE':'SALVAR REPLAY','DECISION':'DECISAO','DRAW':'EMPATE','DEFAULT DATA':'DADOS PADRAO','FILE LOAD':'CARREGAR',
'NO USE':'NAO USAR','KO WON':'VENCEU KO','KO LOSE':'PERDEU KO','TKO WON':'VENCEU TKO','TKO LOSE':'PERDEU TKO','DECISION WON':'VENCEU PONTOS',
'DECISION LOSE':'PERDEU PONTOS','SPACE':'ESPACO','DEL':'APAGA','END':'FIM','NEW DATA':'NOVOS DADOS','PROTEST BOXER':'ASPIRANTE',
'ENGLAND OUT OF RANK':'INGLATERRA SEM RANK','THAILAND TOURNAMENT':'TORNEIO TAILANDIA','THAILAND':'TAILANDIA','KOREA':'COREIA',
'JAPAN TOURNAMENT':'TORNEIO JAPAO','JAPAN OUT OF RANK':'JAPAO SEM RANK','JAPAN RANKER':'JAPAO RANQUEADO','JAPAN TITLE MATCH':'JAPAO TITULO',
'ENGLAND TOURNAMENT':'TORNEIO INGLATERRA','USA OUT OF RANK':'EUA SEM RANK','USA TOURNAMENT':'TORNEIO EUA','KOREA TITLE MATCH':'COREIA TITULO',
'ENGLAND RANKER':'INGLATERRA RANQ.','ENGLAND TITLE MATCH':'INGLATERRA TITULO','USA RANKER':'EUA RANQUEADO','USA TITLE MATCH':'EUA TITULO',
'JAPAN':'JAPAO','ENGLAND':'INGLATERRA','MEXICO':'MEXICO','ITALY':'ITALIA','FRANCE':'FRANCA','SOUTH AFRICA':'AFRICA DO SUL',
'Boxer\'s Road Options':'Opcoes Boxer\'s Road','Options':'Opcoes','Weight':'Peso','Champion':'Campeao','Control Setting':'Controles',
'Free Knock Down':'Quedas livres','Yes':'Sim','No':'Nao','Right':'Direita','Left':'Esquerda','Switch':'Ambidestro','Face':'Rosto','Body':'Corpo',
'Hair':'Cabelo','Mustache':'Bigode','Beard':'Barba','Trunks':'Calcao','Shoes':'Botas','All':'Tudo','Bout':'Lutas','Won':'Vit.','Lost':'Der.',
'Draw':'Empate','Blue Won':'Azul venceu','Red Won':'Vermelho venceu','Are You Sure?':'Tem certeza?','No Data':'Sem dados',
'Japan':'Japao','Brazil':'Brasil','England':'Inglaterra','Thailand':'Tailandia','Korea':'Coreia','United States':'Estados Unidos',
'Germany':'Alemanha','France':'Franca','Italy':'Italia','Spain':'Espanha','Philippines':'Filipinas','Mexico':'Mexico','Netherlands':'Holanda',
'Sweden':'Suecia','Switzerland':'Suica','Poland':'Polonia','Belgium':'Belgica','Ireland':'Irlanda','South Africa':'Africa do Sul',
'New Zealand':'Nova Zelandia','Turkey':'Turquia','Greece':'Grecia','Hungary':'Hungria','Norway':'Noruega','Denmark':'Dinamarca','Finland':'Finlandia',
'Super Middle':'Supermedio','Light Heavy':'Meio-pesado','Minimum':'Minimo','Straw':'Palha','Fly':'Mosca','Bantam':'Galo','Feather':'Pena',
'Light':'Leve','Middle':'Medio','Cruiser':'Cruzador','Heavy':'Pesado',
}
def patch(b, lo=0x370000, hi=0x3a0000):
    b=bytearray(b); done=[]; skip=[]
    for m in re.finditer(rb'(?<=\x00)([^\x00]{1,40})\x00', bytes(b[lo:hi])):
        raw=m.group(1); s=raw.decode('latin1'); core=s.strip(' \n')
        if core not in M: continue
        o=lo+m.start(1)
        pre=s[:len(s)-len(s.lstrip(' \n'))]; suf=s[len(s.rstrip(' \n')):]
        new=(pre+M[core]+suf).encode('ascii')
        # space = original + following zeros, keeping 1 terminator
        e=o+len(raw); z=0
        while b[e+z]==0: z+=1
        room=len(raw)+z-1
        # keep 4-byte alignment if next string starts aligned: don't eat the zero right before next data
        if len(new)<=room:
            b[o:o+len(raw)+z]=new+b'\x00'*(len(raw)+z-len(new)); done.append((hex(o),s,M[core]))
        else:
            short=M[core][:max(0,room-len(pre)-len(suf))]
            skip.append((hex(o),s,M[core],room))
    return bytes(b),done,skip
