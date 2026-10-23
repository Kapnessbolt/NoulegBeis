---
type: home
---

# Home

Vista dal vivo del vault per Obsidian, con i plugin **Tasks** e **Dataview**. Il riepilogo con calendario Outlook è la dashboard [Cockpit](https://claude.ai/artifact/KN8Wp48Ja6vGbShXeTpRgR).

## Scadute

```tasks
not done
path includes projects/
heading includes Attività
due before today
sort by due
```

## Prossimi 7 giorni

```tasks
not done
path includes projects/
heading includes Attività
due after yesterday
due before in 8 days
sort by due
```

## Prossime scadenze (8–60 giorni)

```tasks
not done
path includes projects/
heading includes Attività
due after in 7 days
due before in 61 days
sort by due
```

## Progetti attivi

```dataview
TABLE WITHOUT ID
  file.link AS "Progetto",
  choice(startswith(lower(role), "non coinvolto"), "osservi", "tuo") AS "Ruolo",
  length(filter(file.tasks, (t) => !t.completed)) AS "Aperte",
  length(filter(file.tasks, (t) => t.completed)) AS "Fatte",
  updated AS "Aggiornato"
FROM "projects"
WHERE type = "project" AND status = "attivo"
SORT choice(startswith(lower(role), "non coinvolto"), 1, 0) ASC, updated DESC
```

## Attività senza data

```tasks
not done
path includes projects/
heading includes Attività
no due date
group by filename
```

## Ultimi digest

```dataview
LIST
FROM "journal"
SORT file.name DESC
LIMIT 3
```

## Inbox da smistare

```dataview
LIST
FROM "inbox"
SORT file.name DESC
```
