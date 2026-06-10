
-- 1. Table des rôles personnalisés (Liée à auth_user de Django)
CREATE TABLE `accounts_compteutilisateur` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role` varchar(10) NOT NULL COMMENT 'mentor ou mentore',
  `user_id` int(11) NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Table des profils étudiants (Extensions de l'utilisateur)
CREATE TABLE `profiles_profil` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `photo` varchar(100) DEFAULT NULL,
  `filiere` varchar(100) DEFAULT NULL,
  `niveau` varchar(2) DEFAULT NULL COMMENT 'L1, L2, L3, M1, M2',
  `competences` longtext DEFAULT NULL,
  `lacunes` longtext DEFAULT NULL,
  `user_id` int(11) NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Table des Annonces (Offres et Demandes)
CREATE TABLE `profiles_annonce` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type_annonce` varchar(10) NOT NULL COMMENT 'OFFRE ou DEMANDE',
  `matiere` varchar(100) NOT NULL,
  `format_cours` varchar(15) NOT NULL COMMENT 'EN_LIGNE ou PRESENTIEL',
  `disponibilites` varchar(255) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `auteur_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`auteur_id`) REFERENCES `profiles_profil` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Table des Matchings (Mise en relation)
CREATE TABLE `profiles_matching` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `etat` varchar(20) NOT NULL DEFAULT 'EN_ATTENTE' COMMENT 'EN_ATTENTE, ACCEPTE, REFUSE',
  `date_demande` datetime(6) NOT NULL,
  `annonce_id` bigint(20) NOT NULL,
  `candidat_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`annonce_id`) REFERENCES `profiles_annonce` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`candidat_id`) REFERENCES `profiles_profil` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Table de la Messagerie Instantanée
CREATE TABLE `profiles_message` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `contenu` longtext NOT NULL,
  `date_envoi` datetime(6) NOT NULL,
  `lu` tinyint(1) NOT NULL DEFAULT 0,
  `destinataire_id` int(11) NOT NULL,
  `expediteur_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`destinataire_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`expediteur_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;