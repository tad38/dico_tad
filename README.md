# dico_tad

Création de wordlists à partir de pages web, de fichiers ou de StdIn avec suppression des doublons.

Vous aurez la possibilité de mettre les mots en minuscules, en majuscules ou tel quel, et de les filtrer en fonction de leur taille.

Si vous ne précisez pas de fichier de sortie (-s), la liste sera affichée dans la sortie standard.

## Arguments obligatoires

| Nom | Description |
| - | - |
| `chemin` | Un ou plusieurs chemins de fichiers, dossiers ou URL séparés par des virgules (,). Si vous mettez un tiret (-), c'est la chaîne contenue dans StdIn (entrée standard) qui sera analysée |

## Arguments optionnels

| Nom court | Nom long | Description |
| ------------ | ------------------ | - |
| `-s FICHIER` | `--sortie FICHIER` | Chemin du fichier dans lequel écrire la liste de mots. (par défaut, la sortie se fait sur la sortie standard: StdOut) |
| `-t TAILLE` | `--taille TAILLE` | Taille des mots acceptés. Ex: 2-4 = de 2 caractères à 4 caractères inclus. 0=infini. (Par défaut 2-0) |
| `-r` | `--recursif` | Rechercher aussi dans les sous-dossiers. (uniquement pour un chemin local. Par défaut: non) |
|  | `--maj` | Ajouter les mots convertis en majuscules dans la liste. (Par défaut: non) |
|  | `--min` | Ajouter les mots convertis en minuscules dans la liste. (Par défaut: non) |
|  | `--tel` | Ajouter les mots dans la liste tels qu'ils ont été trouvés. (Par défaut: oui) |
|  | `--acc` | Remplacer les voyelles avec des accents par leur lettre normale. (Par défaut: non) |
