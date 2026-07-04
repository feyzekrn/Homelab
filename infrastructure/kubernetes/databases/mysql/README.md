# MySQL

[<- Back to Databases](../README.md)

MySQL is included because it remains one of the most common databases in full-stack development.

Even if PostgreSQL is the default for new services, MySQL is valuable for compatibility with existing tools, tutorials, CMS systems and applications.

MySQL is a relational database. Like PostgreSQL, it stores structured data in tables and is queried with SQL. It has been a major part of web development for decades and is still the default database for many applications, hosting providers, CMS systems and tutorials.

This homelab does not need MySQL as the default database for new custom services, but it should understand MySQL because real software often assumes MySQL or MariaDB compatibility.

---

## Why It Fits

MySQL is useful for learning compatibility. Many applications are written with MySQL assumptions around SQL syntax, indexes, storage engines or operational tooling. Running MySQL lets the homelab test those applications without forcing everything into PostgreSQL.

It also makes database comparisons practical. ORMs, migrations, backup tools and performance behavior can differ between PostgreSQL and MySQL.

---

## Used For

- MySQL-specific application testing
- common web stack compatibility
- ORM behavior comparison
- migration and backup practice
- learning MySQL/MariaDB ecosystem assumptions

---

## Strengths

- Very common in web application ecosystems.
- Broad tooling and hosting support.
- Strong compatibility target for existing software.
- Useful for learning MySQL-specific backup and replication patterns.

---

## Weaknesses

- Not the preferred default for new custom services in this repo.
- MySQL and PostgreSQL differences can surprise developers who assume "SQL is SQL."
- Serious Kubernetes operation still needs storage, backups, monitoring and upgrade planning.

---

## Application Examples

- Testing applications that assume MySQL or MariaDB as their default database.
- Comparing Prisma, TypeORM, Hibernate or Spring Data behavior between MySQL and PostgreSQL.
- Running common CMS, forum or legacy-style web applications in the cluster.
- Practicing backup and restore workflows with `mysqldump` or operator-managed backups.

---

## Alternatives

| Alternative | Notes |
|---|---|
| MariaDB | Community-driven MySQL-compatible database |
| PostgreSQL | Better default for most new custom services |

---

## Comparison Notes

MySQL is worth running because many real-world projects depend on it. PostgreSQL remains the better default for new custom services in this homelab. MariaDB is a strong alternative when a MySQL-compatible open community stack is preferred.

---

## Runtime Status

MySQL is currently `⚫ Inactive`. It should run when compatibility testing or MySQL-specific learning is needed.

---

## Operator Note

Evaluate the Oracle MySQL Operator or Percona Operator before deciding on a long-term deployment model.

See also: [`../../operators`](../../operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/databases/mysql/
```

---

## Learning Links

- [MySQL documentation](https://dev.mysql.com/doc/)
- [Wikipedia: MySQL](https://en.wikipedia.org/wiki/MySQL)
- [Wikipedia: MariaDB](https://en.wikipedia.org/wiki/MariaDB)
- [Wikipedia: SQL](https://en.wikipedia.org/wiki/SQL)
