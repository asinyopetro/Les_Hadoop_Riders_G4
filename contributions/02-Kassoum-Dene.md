# Kassoum Dene (Youri2k) — Partie présentation

## Sujet (2–3 min)
**HDFS vs système de fichiers local** + **ResourceManager vs NodeManager**.

## Points à dire
1. FS local (NTFS/ext4) = fichier sur **une** machine.
2. HDFS = fichier découpé en **blocs**, répliqués sur plusieurs DataNodes ; NameNode = métadonnées.
3. Quand on lance un job : **RM** alloue les ressources / décide ; **NM** exécute sur chaque worker.
4. Lien avec notre cluster : 1 master (NN+RM) + 5 workers (DN+NM).

## À faire avant le 7 oct
- [ ] Accepter invite : https://github.com/asinyopetro/Les_Hadoop_Riders_G4/invitations
- [ ] Relire Partie 1.2 et 1.3 du rapport
- [ ] Commit + push

## Validation
- [ ] Validé par Kassoum — date : ________
