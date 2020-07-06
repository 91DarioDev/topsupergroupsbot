# TopSupergroupsBot - A telegram bot for telegram public groups leaderboards
# Copyright (C) 2017-2018  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
#
# TopSupergroupsBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TopSupergroupsBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with TopSupergroupsBot.  If not, see <http://www.gnu.org/licenses/>.

buttons_strings = {
    "leaderboard": "classificação",
    "about_you": "sobre você",
    "region": "região",
    "settings": "configurações",
    "info_and_help": "info & ajuda"
}


hello = "Olá!"

choose_group_lang = (
        "Escolha o idioma do grupo. "
        "Seu grupo será adicionado à classificação para o idioma correspondente. "
        "Não minta ou esse grupo será removido")

group_settings = "Configurações do grupo:"
messages_in_groups_position = "— {} mensagens em @{}. Sua posição: {}\n"
have_adult = "Esse grupo tem conteúdo adulto?"
here_group_vote_link = "Este é o link para que os usuários votem neste grupo"
canceled = "Cancelado"
already_this_page = "Você já está nesta página!"

vote_this_group = "id: {}\nusername: @{}\ntitle: {}"
already_voted = "Já votou {} em {}"
vote = "votar"
vote_from_one_to_five = "Classifique esse grupo de 1 a 5 estrelas"
choose_your_lang = "Selecione seu idioma"

group_lang_button = "Idioma do grupo"
adult_button = "Adult Emoji"
vote_link_button = "Vote link"
back = "Voltar"
yes = "Sim"
no = "Não"
cancel = "Cancelar"

this_command_only_private = "{} é somente para conversas privadas"
this_command_only_admins = "{} é somente para o criador ou admins em grupos"
this_command_only_creator = "{} é somente para o criador em grupos"
but_you_can_use_in_private = ".\nMas você pode usar aqui."
button_for_creator = "Este botão é somente para o criador do grupo"
button_for_admins = "Este botão é somente para um admin"
invalid_command = "comando inválido"

cant_vote_this = "Eu não estou nesse grupo. Então, não é possível votar nele!"
registered_vote = "Voto registrado!"
updated_vote = "Voto atualizado!"

choose_region = (
        "Escolha sua região. Será seu filtro padrão de idioma quando "
        "solicitar a classificação")

pre_leadervote = "Ordenada pela média de votos. Tendo, no mínimo, {} votos.\nRegião: {}"
pre_leadermessage = "Ordenada pelas mensagens enviadas nesta semana(UTC).\nRegião: {}"
pre_groupleaderboard = "Principais usuários em ordem de mensagens enviadas nesta semana(UTC) em @{}."
pre_leadermember = "Ordenado pela quantidade de membros.\nRegião: {}"


private_lang_button = "Idioma"
private_region_button = "Região"
private_settings = "Configurações:"
private_digest_button = "Resumo"
private_your_own_digest_button = "Sobre você"
private_groups_digest_button = "Sobre os grupos"
private_digest = "Você recebe um resumo no final de cada semana. É possível habilitar ou desabilitar a qualquer momento"
weekly_own_digest = "Você quer receber estatísticas semanais sobre você?"
hello_name = "Olá, {name}"
digest_of_the_week_global = ("Mais uma semana terminou!\nNesta última semana você enviou {} mensagens "
                             "em {} grupos. Sua posição no ranking global: {}\n")

digest_of_the_week_detail = "— {} mensagens em @{}. Sua posição: {}\n"

generic_leaderboard = (
        "Esscolha um dos critérios para a ordem de classificação.\n" 
        "Sua região: {}. Toque em /region caso queira ver grupos de outras regiões")

by_members = "Por membros"
by_messages = "Por mensagens"
by_votes = "Por votos"


help_commands = (
        "aqui estão os comandos que você pode usar:\n\n"
        "/leaderboard - <i>veja a classificação dos grupos</i>\n"
        "/vote - <i>vote em um grupo</i>\n"
        "/aboutyou - <i>veja estatísticas sobre você</i>\n"
        "/settings - <i>mude suas configurações</i>\n"
        "/feedback - <i>envie um feedback</i>"
)

help_message = "Este bot faz estatísticas e tabelas de classificação sobre grupos e seus membros"

insert_param_vote = (
        "Para votar em um grupo, envie o nome de usuário (independentemente de ter o '@')"
        " depois do comando /vote.\n\nExemplo:\n<code>/vote @NonEntrate</code>")


disable = "Desabilitar"
hey_no_lang_set = (
        "Ei! Você ainda não definiu nenhum idioma. Portanto, em qual região este "
        "grupo deve estar?. Por favor, defina um idioma.")

you_inactive_this_week = "Esta semana você ainda não enviou mensagens em grupos"
this_week_you_sent_this = "Esta semana você já enviou:"
you_globally_this_week = "Você já enviou globalmente {} mensagens em {} grupos durante esta semana. Sua posição em todo o mundo: {}"

unsupported_chat = (
        "Fui programado para participar apenas de grupos públicos. "
        "Este não é um grupo público. Vou embora, tchau!")

banned_until_leave = "Este grupo foi banido. A proibição terminará em {} UTC. \nMotivo: {}.\nEstou saindo."
not_specified = "Não especificado"

group_digest_button = "Resumdo"
group_weekly_digest = (
        "Gostaria de receber um resumo semanal deste grupo?"
        " Você pode mudar de idéia a qualquer momento.")


groups_working = (
        "Deseja que seu grupo faça parte de nossas tabelas de classificação? Basta adicionar este bot em"
         " seu grupo e certifique-se de definir o idioma correto do grupo. O grupo"
         " será adicionado à região que você especificou com o idioma.\n"
         "Se o seu grupo tiver conteúdo adulto, selecione a opção correta em /settings. Por favor"
         " certifique-se de inserir apenas as informações corretas ou podemos banir seu grupo do nosso bot.\n"
         "Não aplicamos nenhum tipo de censura sobre tópicos, mas podemos proibir grupos que trapacerem"
         " nas tabelas de classificação.\nEm /settings, você encontrará o link para redirecionar os usuários para"
         " votar no seu grupo.\n\n"
        "<b>COMANDOS SUPORTADOS EM GRUPOS</b>:\n"
        "/settings - <i>definiar as configurações do grupo</i>\n"
        "/groupleaderboard - <i>recebe uma mensagem com a classificação dos usuários que mais enviaram "
        "mensagens no grupo durante a semana (UTC). parâmetro opcional: [número da página]</i>\n"
        "/grouprank - <i>Veja o ranking do grupo</i>"
)

weekly_groups_digest = (
        "Olá! Mais uma semana terminou. Aqui estão algumas estatísticas do grupo:\n\n"
        
        "-- POR MENSAGEM --\n"
        "mensagens enviadas na última semana: {}\n"
        "mensagens enviadas nesta semanan: {}\n"
        "diferença: {}  percentual: {}\n"
        "posição na última semana: {}\n"
        "posição nesta semana: {}\n\n"
        
        "-- POR MEMBROS --\n"
        "membros da última semana: {}\n"
        "membros nesta semana: {}\n"
        "diferença: {}  percentual: {}\n"
       "posição na última semana: {}\n"
        "posição nesta semana: {}\n\n"
        
        "-- PELA MÉDIA DE VOTOS --\n"
        "média e número de votos da última semana: {}{}|({})\n"
        "média e número de votos desta semana: {}{}|({})\n"
        "posição na última semana: {}\n"
        "posição nesta semana: {}\n\n"
        
        "-- BY ACTIVE USERS --\n"
        "usuários ativos da última semana: {}\n"
        "usuários ativos desta semana: {}\n"
        "diferença: {}  percentual: {}\n"
       "posição na última semana: {}\n"
        "posição nesta semana: {}\n\n"
        
        "PRINCIPAIS USÁRIOS DESTA SEMANA:\n"
        )

added_again = "Olá! Você quer verificar as configurações do grupo novamente?"

feedback_message = ("A única maneira de enviar um feedback é enviar sua mensagem como resposta a esta mensagem"
        ".\n\nVocê pode enviar qualquer tipo de mensagem ou mídia.")

thanks_feedback = "Feedback enviado com sucesso! obrigado!"

feedback_flood = ("Desculpe, você já enviou muitos feedbacks. Aguarde uma resposta primeiro ou aguarde um pouco."
        "Não há como enviar esse feedback")

from_developer = "Esta é uma mensagem do desenvolvedor do bot."

feedback_reply = "Responder"

unrecognized_button = ("uma mensagem iniciando e terminando com esse caractere é tratada como um botão. "
        "O botão que você pressionou é inválido. Enviei a você um teclado atualizado.\n\nSe você estiver "
        "enviando essa mensagem apenas como mensagem, acrescente outro caractere no início ou no final.")

updating_buttons = "Atualizando botões"

latest_update = "Atualização"
seconds_ago = "{} segundos atrás"
about_minutes_ago = "cerca de {} minutos atrás"
about_hours_ago = "cerca de {} horas atrás"
seconds_ago_short = "{} seg atrás"
about_minutes_ago_short = "aprox {} min atrás"
about_hours_ago_short = "aprox {}h atrás"

group_rank = {
    "title": "<b>RANKING DO GRUPO:</b>",
    "by_messages": "<b>Tabela de classificação ordenada por mensagens enviadas durante a semana atual</b> (região: <code>{}</code>):",
    "by_members": "<b>Classificação ordenada por quantidade de membros</b> (região: <code>{}</code>):",
    "by_votes": "<b>Classificação ordenada por média de votos</b> (região: <code>{}</code>):",
    "position": "- Posição: {}",
    "updated": "<i>{}: {}</i>",
    "None": "Infelizmente este grupo não está em nenhuma tabela de classificação",
    "messages": "- mensagens: {}",
    "members": "- membros: {}",
    "votes": "- média|número de votos: {}|({})"
}

feedback = "feedback"
source_code = "código fonte"
commands = "comandos"
how_to_use_in_groups = "uso em grupos"


category = "Categoria"
choose_group_category = "Escolha a categoria que melhor se encaixa nesse grupo. Não minta ou proibiremos o grupo."
categories = {
    'news': 'notícias',
    'science_and_education': 'ciência e educação',
    'religion': 'espiritualidade',
    'entertainment': 'entretenimento',
    'family_and_home': 'família e casa',
    'sport': 'esportes',
    'art_and_culture': 'arte e cultura',
    'politics': 'política',
    'information_technology': 'Tecnologia',
    'game_and_apps': 'jogos e aplicativos',
    'love': 'relacionamento',
    'tourism': 'turismo',
    'economics': 'economia'
}
filter_by_category = 'filtrar categoria'
choose_category_to_filter = "escolha uma das seguintes categorias para filtrar a classificação"
remove_filter = "remover filtro"

change_vote = "mudar voto"

advanced_commands = "Comandos avançados"

advanced_commands_text = (
    "<b>Comandos avançados:</b>\n\n"
    "/leadervote - <i>tabela de classificação ordenada por votos (parâmetros opcionais: [p = (número da página)] [c = (número da categoria)])</i>\n"
    "/leadermember - <i>tabela de classificação ordenada pelos membros (parâmetros opcionais: [p = (número da página)] [c = (número da categoria)]</i>\n"
    "/leadermessage - <i>cabeçalho ordenado por mensagens (parâmetros opcionais: [p = (número da página)] [c = (número da categoria)]</i>\n\n"
    "O número da categoria pode ser obtido contando os botões das categorias, começando da esquerda para a direita\n\n"
    "/grouprank - <i>/grouprank [nome de usuário do grupo]</i>\n"
    "/groupleaderboard - <i>/groupleaderboard [nome de usuário do grupo]</i>"
)

groupleaderboard_command_error = "<b>Erro:</b>\nuse o comando dessa forma:\n\n<code>{} [número da página(opcional)]</code>"

avdanced_leaderboard_command_error = "<b>Erro:</b>\nuse o comando dessa forma. Parâmetros são opcionais:\n\n<code>{} [p=(número da página)] [c=(número da categoria)]</code>"

error_param_group_rank_private = (
    "<b>Error:</b>\nyou should write as parameter of this command the username of the group that you want to check the rank. "
    "You can put or not the \"@\" (it doesn't matter).\n\nExample: <code>/grouprank my_favorite_group</code>"
)

cant_check_this = "Sorry, @{} is not in our database."

error_param_group_leaderboard_private = (
    "<b>Error:</b>\nyou should write as parameter of this command the username of the group that you want to check the groupleaderboard. "
    "You can put or not the \"@\" (it doesn't matter).\n\nExample: <code>/groupleaderboard my_favorite_group</code>\n\n"
    "Optionally you can jump directly to a page adding the parameter <code>p=[page number]</code>.\n\nExample: <code>/groupleaderboard my_favorite_group p=26</code>"
)

check_in_private = "Veja na conversa privada"

official_channel = "canal oficial"
donate = "donate"
donate_intro = ("This bot is free, opensource and developed for telegram communities.\n\nAnyways the developement required and still "
    "requires a lot of time and money to pay servers. We will be very happy if you can help us with project with a little donation.\n\n"
)
something_went_wrong = "Ops! something went wrong."
