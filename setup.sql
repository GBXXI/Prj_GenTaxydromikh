-- SQLite
DROP TABLE IF EXISTS Recipients;
DROP TABLE IF EXISTS CarbonCopy;
DROP TABLE IF EXISTS RecipientsEmail;
DROP TABLE IF EXISTS CarbonCopyEmails;
DROP VIEW IF EXISTS 'Recipients Email';
DROP VIEW IF EXISTS 'Included Email';


PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Recipients(
        recipient_id INTEGER PRIMARY KEY,
        recipient_name TEXT NOT NULL UNIQUE

    )
;

CREATE TABLE IF NOT EXISTS RecipientsEmail(
        email_id INTEGER,
        email TEXT NOT NULL UNIQUE,

        FOREIGN KEY (email_id) REFERENCES Recipients(recipient_id) ON DELETE CASCADE
    )
;

CREATE TABLE IF NOT EXISTS CarbonCopy(
        included_id INTEGER PRIMARY KEY,
        included_name TEXT NOT NULL UNIQUE
    )
;

CREATE TABLE IF NOT EXISTS CarbonCopyEmails(
        email_id INTEGER,
        email TEXT NOT NULL UNIQUE,

        FOREIGN KEY (email_id) REFERENCES CarbonCopy(included_id) ON DELETE CASCADE
    )
;


INSERT INTO Recipients(
        recipient_id, recipient_name
    )

        VALUES
            (1, 'Default Recipient')
;

INSERT INTO RecipientsEmail(
        email_id, email
    )

    VALUES
        (1, 'Default_Recipient@test.test')
;

INSERT INTO CarbonCopy(
        included_id, included_name
    )

    VALUES
        (1, 'Default CarbonCopy')
;

INSERT INTO CarbonCopyEmails(
        email_id, email
    )

    VALUES
        (1, 'Default_CarbonCopy@test.test')
;

CREATE VIEW IF NOT EXISTS 'Recipients Email' AS
    SELECT DISTINCT
        (CASE WHEN e.email_id = 1 THEN e.email END) 'Default Recipient'

    FROM RecipientsEmail e
    ORDER BY 'Default Recipient' DESC
;

CREATE VIEW IF NOT EXISTS 'Included Email' AS
    SELECT DISTINCT
        (CASE WHEN e.email_id = 1 THEN e.email END) 'Included Recipient'

    FROM CarbonCopyEmails e
    ORDER BY 'Included Recipient' DESC
;

CREATE INDEX "Recipients.recipientname"
    ON Recipients(recipient_name)
;

CREATE INDEX "Recipients.recipientid_recipientname"
    ON Recipients(recipient_id, recipient_name)
;

CREATE INDEX "RecipientsEmail.email"
    ON RecipientsEmail(email)
;

CREATE INDEX "RecipientsEmail.emailid_email"
    ON RecipientsEmail(email_id, email)
;

CREATE INDEX "CarbonCopy.included_name"
    ON CarbonCopy(included_name)
;

CREATE INDEX "CarbonCopy.includedid_includedname"
    ON CarbonCopy(included_id, included_name)
;

CREATE INDEX "CarbonCopyEmails.email"
    ON CarbonCopyEmails(email)
;

CREATE INDEX "CarbonCopyEmails.emailid_email"
    ON CarbonCopyEmails(email_id, email)
;
