
CREATE TABLE affaire_r (
    id bigint NOT NULL,
    id_utilisateur integer,
    date_reception date,
    date_fermeture date,
    is_archivable boolean DEFAULT false NOT NULL
);
