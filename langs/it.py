# TopSupergroupsBot - A telegram bot for telegram public groups leaderboards
# Copyright (C) 2017  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
#
# TopSupergroupsBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TopSupergroupsBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TopSupergroupsBot.  If not, see <http://www.gnu.org/licenses/>.


choose_group_lang = ("Scegli la lingua del gruppo. "
					"Il gruppo verrà aggiunto nelle classifiche in base alla lingua inserita. "
					"Non mentire o banneremo il gruppo")
group_settings = "Impostazioni gruppo:"
messages_in_groups_position = "— {} messaggi in @{}. Posizione: {}\n"
have_adult = "Questo gruppo ha contenuti per adulti?"
here_group_vote_link = "Questo è il link per indirizzare gli utenti direttamente a votare questo gruppo."
canceled = "Anullato"
already_this_page = "Sei già in questa pagina!"

vote_this_group = "id: {}\nusername: @{}\titolo: {}"
already_voted = "Già votato {} il {}"
choose_your_lang = "Seleziona la tua lingua"

group_lang_button = "Lingua gruppo"
adult_button = "Emoji adulti"
vote_link_button = "Link per voto"
back = "Indietro"
yes = "Sì"
no = "No"
cancel = "Annulla"

this_command_only_private = "Il comando che hai dato è solo per le chat private"
this_command_only_admins = "Questo comandi è solo per il creatore o gli admin nei gruppi"
this_command_only_creator = "Questo comando è solo per il creatore nei gruppi"
button_for_creator = "Questo bottone è solo per il creatore"
button_for_admins = "Questo bottone è solo per gli admin"
invalid_command = "Comando non valido"

cant_vote_this = "Non sono in questo gruppo, quindi non puoi votarlo, mi spiace!"
registered_vote = "Voto registrato!"
updated_vote = "Voto aggiornato!"

choose_region = ("Scegli la tua regione. Sarà il filtro di default per la lingua dei gruppi quando "
				"richiedi una classifica")

pre_leadervote = "Top supergruppi ordinati per media voti. Hanno almeno {} voti.\nRegione: {}"
pre_leadermessage = "Top supergruppi ordinati per numero di messaggi inviati questa settimana (UTC).\nRegione: {}"
pre_groupleaderboard = "Top utenti ordinati per numero di messaggi inviati durante questa settimana (UTC) in questo gruppo."
pre_leadermember = "Top supergruppi ordinati per numero di membri.\nRegione: {}"


private_lang_button = "Lingua"
private_region_button = "Regione"
private_settings = "Impostazioni:"
private_digest_button = "Resoconto"
private_your_own_digest_button = "Su di te"
private_groups_digest_button = "Sui gruppi"
private_digest = "Puoi ricevere un resoconto alla fine di ogni settimana. Abilita o disabilita quando vuoi"
weekly_own_digest = "Vuoi ricevere statistiche su di te ogni volta che una settimana finisce?"
digest_of_the_week_global = ("Un'altra settimana è passata!\nDurante la scorsa settimana hai inviato in totale {} messaggi "
					"in {} gruppi. Posizione: {}\n")

digest_of_the_week_detail = "— {} messaggi in @{}. Posizione: {}\n"

generic_leaderboard = ("Scegli uno dei seguenti criteri per ordinare la classifica.\n" 
					"Queste sono delle scorciatoie per la prossima volta se vuoi fare prima:\n\n"
					"/leadermember - <i>ordinata per numero di membri</i>\n"
					"/leadermessage - <i>ordinata per numero di messaggi inviati in questa settimana</i>\n"
					"/leadervote - <i>ordinata per media voti</i>\n\n"
					"La tua regione: {}. Premi /region per vedere gruppi di altre regioni.")

by_members = "Per membri"
by_messages = "Per messaggi"
by_votes = "Per voti"

help_message = ("Questo bot fa statistiche e classifiche di gruppi pubblici e i loro utenti.\n"
			"Questi sono i comandi che puoi usare:\n\n"
			"/leaderboard - <i>guarda classifiche dei gruppi</i>\n"
			"/vote - <i>vota un gruppo</i>\n"
			"/aboutyou - <i>ottieni statistiche su di te</i>\n"
			"/settings - <i>cambia le tue impostazioni</i>\n\n"
			"Se sei un admin di un gruppo potresti essere interessato in "
			"<a href=\"{}\">come usare il bot nei gruppi</a>")

insert_param_vote = ("Per votare un gruppo invia il suo username (non importa se c'è o no '@')"
				" come parametro del comando /vote.\n\nEsempio:\n<code>/vote @NonEntrate</code>")


disable = "Disabilita"
hey_no_lang_set = ("Hey! Non avete impostato nessuna lingua, quindi in che regione delle classifiche "
				"devo mettere questo gruppo?. No, seriamente, imposta la lingua.")

you_inactive_this_week = "Questa settimana ancora non hai inviato messaggi nei gruppi"
this_week_you_sent_this = "Questa settimana hai già inviato:"
you_globally_this_week = "In totale hai già inviato {} messaggi in {} gruppi in questa settimana. Posizione: {}"

unsupported_chat = ("Sono stato programmato per far parte solo di gruppi pubblici. "
					"Questo non è un gruppo pubblico. Vi saluto!")

banned_until_leave = "Questo gruppo è stato bannato. Il ban scadrà il {} UTC.\nMotivo: {}.\nVi saluto."
not_specified = "Non specificato"

group_digest_button = "Resoconto"
group_weekly_digest = ("Vuoi ricevere un resoconto di questo gruppo ogni volta che una settimana finsice?"
					" Puoi ripensarci in qualsiasi momento.")


groups_working = ("Vuoi che il tuo gruppo faccia parte delle nostre classifiche? Ti basta solo aggiungere"
				" questo bot nel tuo gruppo e impostare la giusta lingua del gruppo. Il gruppo sarà "
				"aggiunto nella regione di classifiche che hai specificato con la lingua.\n"
				"Se il tuo gruppo ha contenuti per adulti, selezionalo in /settings. Per piacere "
				"assicurati di inserire solamente valore corretti o potremmo bannare il tuo gruppo dal nostro bot.\n"
				"Non applichiamo nessun tipo di censura sugli argomenti, ma banniamo i gruppi che barano "
				" nelle classifiche.\nIn /settings potrai perfino trovare il link per indirizzarei tuoi utenti "
				" a votare direttamente il tuo gruppo.\n\n"
				"<b>COMANDI SUPPPORTATI NEI GRUPPI</b>:\n"
				"/settings - <i>impostazioni gruppo</i>\n"
				"/groupleaderboard - <i>ottieni la classifica degli utenti che hanno scritto "
				"più messagi nel gruppo durante la settimana corrente (UTC)</i>")

weekly_groups_digest = ("Ciao!	Un'altra settimana è passata. Ecco alcune statistiche di questo gruppo:\n\n"
					"messaggi inviati la scorsa settimana: {}\n"
					"messaggi inviati questa settimana: {}\n"
					"differenza: {}  in percentuale: {}\n\n"
					"membri la scorsa settimana: {}\n"
					"membri questa settimana: {}\n"
					"differenza: {}  in percentuale: {}\n\n"
					"media e numero di voti la scorsa settimana: {}|({})\n"
					"media e numero di voti questa settimana: {}|({})\n\n"
					"utenti attivi la scorsa settimana: {}\n"
					"utenti attivi questa settimana: {}\n"
					"differenza: {}  in percentuale: {}\n\n"
					"TOP UTENTI DELLA SETTIMANA:\n"
					)

added_again = "Ciao! Vuoi dare un'occhiata di nuovo alle impostazioni del gruppo?"
