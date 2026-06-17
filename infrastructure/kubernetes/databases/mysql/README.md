# MySQL

[<- Back to Databases](../README.md)

MySQL is included because it remains one of the most common databases in full-stack development.

Even if PostgreSQL is the default for new services, MySQL is valuable for compatibility with existing tools, tutorials, CMS systems and applications.

---

## Used For

- MySQL-specific application testing
- common web stack compatibility
- ORM behavior comparison
- migration and backup practice

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
