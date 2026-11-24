Voce vai traduzir dialogos do jogo de PS2 "Hajime no Ippo 2: Victorious Road" (boxe, anime Hajime no Ippo) do JAPONES para PORTUGUES DO BRASIL.

Arquivo de entrada: /home/claude/ippo/chunks/cNN.json  (lista de {"id": numero, "jp": texto})
Arquivo de saida:   /home/claude/ippo/out/cNN.json   (objeto JSON {"<id>": "texto em portugues", ...} com TODOS os ids da entrada)
Validador:          python3 /home/claude/ippo/check.py NN

Leia a entrada inteira (use Read; se for grande, por partes). Traduza TODOS os itens, voce mesmo, com qualidade (nada de traducao automatica por script). Escreva a saida aos poucos se precisar (por exemplo, monte partes em arquivos /home/claude/ippo/out/cNN_parteX.json e depois junte com python num unico out/cNN.json). Rode o validador e corrija ate dar "com problema 0". Nao mexa em arquivos de outros blocos.

REGRAS OBRIGATORIAS (o validador confere):
1. Codigos de controle: mantenha EXATAMENTE os mesmos codigos, na mesma ordem e quantidade: `_w` (pausa/espera), `_tc` (troca de pagina da caixa de texto), `_mf[...]` (copie igual), `{K0}`, `{K1}`... (copie igual, sao trechos protegidos). Coloque cada `_w` no fim da frase/trecho equivalente. `_tc` costuma ficar sozinho numa linha, como no original — mantenha a mesma estrutura de quebras de linha ao redor dele.
2. Quebras de linha (\n): cada linha visivel pode ter no MAXIMO 46 caracteres (sem contar os codigos). Se a frase em portugues ficar longa, quebre em mais linhas, mas no maximo 4 linhas por pagina (pagina = trecho entre `_tc`). Se nao couber, resuma um pouco.
3. SEM ACENTOS e sem cedilha (a fonte do jogo nao tem): escreva "voce", "nao", "forca", "esta", "e" (para "é"), "campeao", "coracao". Use so caracteres ASCII comuns. Nada de japones, nada de caracteres full-width (troque "・・・" por "...", "！" por "!", "ＧＯ" por "GO" etc.).
4. Nao deixe nenhum item vazio. Mesmo onomatopeias ("ふむ" -> "Hmm", "うむ" -> "Certo", "ハァハァ" -> "Haa... haa...") devem virar portugues.

ESTILO:
- Portugues brasileiro natural e falado, como uma boa legenda de anime. Mantenha a personalidade de cada fala: o velho treinador (fala com "じゃ", "わし") e duro e rabugento ("moleque", "seu idiota", "Entendeu?!"); o sotaque de Osaka ("や", "で", "ワレ", "アカン") vira um jeito mais malandro/informal ("tu", "bora", "mano"); Takamura e arrogante e escrachado; Aoki e Kimura sao brincalhoes.
- O jogador e um boxeador novato criado pelo usuario; trate por "voce"/"tu" conforme o tom.
- Glossario (use sempre igual): 会長/鴨川会長 = "o Presidente" / "Presidente Kamogawa" (quando falam dele); 鴨川ジム = "Academia Kamogawa"; 鷹村(守) = Takamura (Mamoru); 青木(勝) = Aoki (Masaru); 木村(達也) = Kimura (Tatsuya); 八木 = Yagi; 篠田 = Shinoda; 宮田 = Miyata; 千堂 = Sendo; 伊達 = Date; 一歩/幕之内 = Ippo / Makunouchi; 板垣 = Itagaki; 沢村 = Sawamura; ヴォルグ = Volg; ドクター = "o doutor"; コーチ = "o tecnico"; トレーナー = "treinador"; ジム = "academia"; プロテスト = "teste profissional"; デビュー戦 = "luta de estreia"; 新人王(戦) = "(torneio) Novato do Ano"; 東日本新人王 = "Novato do Ano do Leste do Japao"; ランカー = "ranqueado"; ランキング = "ranking"; チャンピオン = "campeao"; タイトルマッチ = "luta pelo titulo"; 防衛(戦) = "defesa (de titulo)"; 計量 = "pesagem"; 減量 = "perder peso"/"corte de peso"; ウェイトオーバー = "acima do peso"; スパーリング = "sparring"; ロードワーク = "corrida"; ミット打ち = "manopla"; サンドバッグ = "saco de pancada"; スタミナ = "folego"; ガッツ = "garra"; ラウンド = "round"; ＫＯ = "nocaute"/"KO"; ダウン = "queda" ou "knockdown"; 日本 = Japao; 東洋太平洋/ＯＰＢＦ = "Oriental e Pacifico (OPBF)"; 世界 = "mundial".
- Nomes de pessoas: ordem ocidental e romanizacao Hepburn sem macron (Takamura, Kimura...). Nomes de golpes conhecidos: デンプシーロール = "Dempsey Roll", ジョルト = "Jolt", ガゼルパンチ = "Gazelle Punch", コークスクリュー = "Corkscrew".

No final responda apenas: o numero do bloco, quantos itens traduziu e a ultima linha do validador.
