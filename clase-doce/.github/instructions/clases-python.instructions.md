---
applyTo: "**/*.py"
description: "Usar cuando se creen o modifiquen clases Python. Aplicar POO disciplinada, encapsulamiento, validacion de invariantes, constructores que solo creen objetos consistentes y preguntas de negocio cerradas si faltan reglas."
---
# Estilo para Clases Python

Cuando generes o refactorices clases Python en este proyecto, sigue estas reglas para aplicar Programación Orientada a Objetos disciplinada, encapsulamiento, validación de invariantes y constructores que solo creen objetos consistentes. Si faltan reglas de negocio, haz preguntas cerradas de sí/no, una a una.

## Principios Generales
- Aplicar buenas prácticas de POO y estilo disciplinado de Python.
- Proteger el estado interno: no expongas atributos mutables públicamente salvo motivo explícito.
- Objetos válidos desde el nacimiento: el constructor debe aceptar solo datos que permitan instancias consistentes.
- Validar entradas en constructor y operaciones públicas que puedan romper invariantes.
- Fallar temprano con excepciones claras (`ValueError`, `TypeError`) si datos no cumplen reglas del dominio.
- Mantener encapsulamiento: usar atributos con `_` y exponer acceso controlado vía `@property`.
- Evitar setters que permitan estados inválidos intermedios.
- Extraer validaciones complejas a métodos privados con nombres claros.
- Evitar clases anémicas: objetos deben proteger invariantes y tener comportamiento propio.
- No usar `dataclass` para entidades con invariantes importantes o encapsulamiento fuerte, salvo pedido explícito.
- Usar nombres claros, type hints y métodos pequeños con una sola responsabilidad.
- Evitar lógica duplicada: centralizar validaciones reutilizables.
- No agregar comentarios redundantes: el código debe ser legible por estructura y nombres.
- Aplicar SOLID: SRP, OCP, LSP, ISP, DIP.
- Identificadores únicos (ej. `id`) deben ser inmutables: solo getters, sin setters.
- Extraer validaciones a clases/módulos dedicados (ej. `AlumnoValidator`) para reutilización y reducir acoplamiento.
- Evitar bugs comunes como indentación incorrecta en métodos especiales (`__str__`, `__eq__`, etc.).

## Criterios de Diseño
- Cada método público debe preservar consistencia del objeto.
- No dejar objetos parcialmente inicializados.
- Para colecciones mutables internas, no devolver referencias directas; usar copias o vistas inmutables.
- Priorizar claridad del dominio sobre conveniencia superficial.

## Cuando Faltan Reglas de Negocio
- Hacer preguntas cerradas (sí/no) una a una.
- Si no conviene frenar, asumir regla lógica y conservadora, indicando suposición brevemente.

## Getters, Setters, Validaciones y Niveles de Visibilidad
- Usar `@property` para getters controlados de atributos privados.
- Implementar `@property.setter` solo si necesario, con validaciones para preservar invariantes.
- Atributos internos: privados con `_`.
- Validar en setters/métodos que modifiquen estado, fallando temprano.
- Evitar setters arbitrarios; preferir métodos específicos descriptivos.
- Para inmutables: solo getters.
- Extraer validaciones a clases dedicadas (ej. `AlumnoValidator`) para reutilización y adherir a SRP. Evita acoplamiento, permite uso en otras clases sin duplicar código, enfoca responsabilidad principal.

## Métodos Especiales
- Implementar `__str__` para representación legible al usuario (ej. `print(obj)`).
- Implementar `__repr__` para representación oficial/debugging, idealmente evaluable para recrear objeto (ej. `repr(obj)`).
- Asegurar indentación correcta: definir fuera de otros métodos para evitar código muerto.

## Resultado Esperado
Al crear una clase nueva, debe mostrar:
- Encapsulamiento real.
- Validación explícita.
- Invariantes protegidas.
- Constructor seguro.
- API pública pequeña y coherente.
- `__str__` y `__repr__` apropiados.