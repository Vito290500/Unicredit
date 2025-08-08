FINHUB CREDIT BANK - PLATFORM

Per una corretto avvio del progetto ci sono alcuni passaggi importanti da seguire:

1. Istallazione della cartella in formato zip presente sul link del progetto. 
2. Installazione ultima versione di docker:

NOTA BENE:
l'ultima versione di docker potrebbe richiedere l'aggiornamento del WSL(Sottosistema Windows per Linux), 
non server installarlo prima di docker, una volta completata l'installazione di docker e fatto il primo avvio 
sarà lui stesso a richiederlo, qualora non venisse richiesto l'installazione è andata a buon fine e potete 
saltare questo passaggio altrimenti se richiesto per aggiornare il WSL basta semplicemente aprire powershell 
eseguendolo con i permessi di amministratore e poi runnare questo comando:

- wsl --update 

una volta terminato aprite docker e dovreste vedere la home dell'applicazione.

3. Aprite la cartella del progetto con visual studio code(se non ce l'avete si consiglia di scaricarlo) e
aprite un nuovo terminale direttamente su visual code e runnate il seguente comando:

- docker-compose build

il comando ci impiegherà diverso tempo poichè costruirà l'immagine con tutte le dipendenze necessarie al
progetto e una volta terminato vedrete una scritta di successo "done" 

4. Successivamente runnate i seguenti comando:

- docker-compose up -d 

- docker-compose exec web python manage.py createsuperuser 

Questo comando vi richiederà di inserire email e password per la creazione di un utente con privilegi 
di admin (questo comando è importante in quanto vi consentirà di accedere alla sezione admin), potete
tranquillamente inventare email e password servono solo per accedere alla sezione admin. (si consiglia
vivamente di segnare le credenziali inserite, perchè serivanno più avanti)

- docker-compose up

una volta fatto potrete aprire il browser e navigare al link del progetto "localhost:8000"

5. Vedrete la sezione login, dovrete prima cliccare su registrati per poter creare l'account.

NOTA BENE: al fine di riuscire a visualizzare correttamente tutte le funzionalità della piattaforma 
è consigliato la creazione di due account diversi purchè almeno il primo è creato con un email reale 
di cui avete accesso al fine di visionare il sistema di registrazione.

Il sistema di registrazione invia in automatico un email all'email inserita (funziona perfettamente con 
email gmail per questa versione, con gli altri tipi di domini potrebbe non funzionare correttamente quindi 
si consiglia di usare gmail). All'interno dell'email ricevuta ci sarà un pulsante che vi renderizzerà ad 
un link sicuro grazie all'utilizzo del Token Jwt di accesso e cliccando verrà attivato l'account. 

Se per qualisasi motivo non dovesse arrivarvi nessuna email controllate nella sezione spam, altrimenti 
inserite questo link "localhost:8000/admin" e vi comparirà la sezione di accesso all'area admin, inserite la 
vostra email e password inserita durante la creazione del superuser con il comando di prima citato. 

Una volta all'interno dell'admin per attivare manualmente l'account basta cliccare su users in basso a sinistra,
poi cliccare sull'email da attivare e poi spuntare il checkbutton "is_active" e cliccare su "save" e ora potete 
accedere alla piattaforma.

6. Dopo aver creato i due account, nella sezione admin cliccando su bank account e su ciascuno dei due inserite
delle cifre fittizie al balance che di default è 0 in modo da poter visionare il funzionamento del bonifico, dove
vi servirà sempre la sezione admin per utilizzare le coordinate corrette per il bonifico sempre visibile nella tabella
back account o accounts.

Una volta eseguiti correttamente tutti questi passaggi potete visionare tranquillamente l'intera piattaforma e 
utilizzare le funzionalità implementate. 












