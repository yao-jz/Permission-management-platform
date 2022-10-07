# Permission-management-platform

A lightweight enterprise common permission platform, with front-end in Vue and back-end in Django

## Introduction

This is the assignment in the Software Engineering Course at Tsinghua University, and this project is mainly designed by Kuaishou.

## Functions

We implemented a common privilege management system in RBAC classical model, which can provide standardized services for multiple business systems (customers). The core functions are as follows:

1. Multi-application support. The configuration (data) and use of permissions for each application are isolated from each other.
2. Permission definition has scalable modeling and implementation.
  1. Permission targets can support multiple types (e.g., URLs, menus, buttons, tables, form columns, database tables, database fields, etc.);
  2. Permission operations can be of various types (e.g. access, add, delete, edit, approve, deny).
3. Role definition support. A role can be associated with multiple permissions, and a permission can be associated with multiple roles, and all associated permissions can be queried by role, and all used roles can be queried by permission.
4. User definition support. A role can be associated with multiple users, a user can be associated with multiple roles, all roles and permissions of a user can be queried by the user, and all users with the role can be queried by the role.
5. Permission query API: After the permission management and definition, the remote business system can get specific application, specific user, and specific type of permission (optional) through the API.
6. Authorization management support (TBD, optional). Realize application authorization and permission approval process definition, support two roles of applicant and approver, and support the flow of approval status.

## Potential Users

All systems, front and back-end developers and business (including operations) personnel within the enterprise. All systems have the need for permission control, and the Enterprise Common Permissions Platform provides these systems with a quick and universal access point and expansion capability, eliminating the need for personnel from other systems to build their own permissions management capabilities.
It can also be quickly accessed, configured and used.
