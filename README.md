# dap
Il tool fornisce tre comandi:
* dap create
* dap clone
* dap addmodule

È possibile utilizzare l'help con 
`dap --help`

## dap create
dap create crea un nuovo progetto nella directory corrente; inizializza repository git e crea ambiente conda.
### comandi
`dap create [--usesnakemake --usemake --usebmake] ProjectName ProjectVersion`
* ProjectName: nome del progetto, che corrisponderà alla directory creata e al nome del repository git inizializzato.
* ProjectVersion: versione iniziale del progetto; viene creata cartella dataset/{ProjectVersion}.
* [--usesnakemake]: inizializza progetto con file necessari per usare snakemake. Default: **True**.
* [--usemake --usebmake]: inizializza progetto con file necessari per usare makefile o bmake. Default: **False**.

## dap clone
Crea una nuova versione del progetto clonando una versione esistente.
Deve essere eseguito all'interno della directory del progetto.
### comandi
`dap clone SourceVersion NewVersion`
* SourceVersion: Nome della versione del progetto.
* NewVersion: Nome della nuova versione del progetto.

Il comando crea una nuova directory *PRJ_ROOT/dataset/{NewVersion}*. In questa, per ogni link contenuto in *PRJ_ROOT/dataset{SourceVersion}*:
* Se il link si riferisce ad un file non versionato: copia il link
* Se il link si riferisce ad un file versionato: genera nuova copia del file versionato nella directory originale e aggiunge link nella directory della versione.
**Per convenzione i file versionati terminano per _{VersionName}.**

## dap addmodule
Importa un progetto esterno all'interno del progetto corrente come modulo, clonandolo da un repository remoto.
Il modulo viene aggiunto come inner repository al repository del progetto.
### comandi
`dap addmodule RepoUrl ProjectVersion ModuleVersion`
* RepoUrl: URL del repository remoto.
* ProjectVersion: path della directory dell versione del progetto all'interno della quale si vuole importare il modulo, relativo a PRJ_ROOT. Per la struttura generale dei progetti dev'essere un path del tipo **dataset/{ProjectVersion}**
* ModuleVersion: nome della versione del modulo che vogliamo importare.

### Progetto conforme
Il progetto da importare come modulo deve essere conforme alla struttura dei progetti generati con dap. In particolare deve contenere la directory *INNER_PRJ_ROOT/dataset/{ModuleVersion}*

Il comando, per ogni link simbolico nella directory *INNER_PRJ_ROOT/dataset/{ModuleVersion}*, crea un link simbolico nella directory *PRJ_ROOT/{ProjectVersion}/{ModuleName}*
