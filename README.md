# Scraping PLUTO TV

Sitio a realizar el scraping: https://pluto.tv

## Objetivo:

### De la seccion On Demand:

Obtener todas las películas y series. Obtener la metadata de cada contenido:
- título ✅
- año (No se encontraba en la web)
- sinopsis ✅
- link ✅
- duración (solo para movies). ✅

> [!NOTE]  
> Separe las peliculas/series por categorias

<details><summary>Ejemplo categoria la_mejor_compañía_movies</summary>

```json
"la_mejor_compañía_movies": {
        "count": 19,
        "movies": [
            {
                "titulo": "Pet Obsessed",
                "metadatos": [
                    "TV-G",
                    "News & Information",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/series/645ab1ce5348f4001a21019c/details?lang=en",
                "descripcion": "Con clips ridículos, cortos digitales y toneladas de pelusa; estas son las mascotas más escandalosas y francas de Internet... Tu nueva obsesión."
            },
            {
                "titulo": "Yo amo a Shakey",
                "metadatos": [
                    "PG",
                    "Children & Family",
                    "1hr 42 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/5f3fd896ad190c001a52e6da/details?lang=en",
                "descripcion": "JT O’Neil, con su hija de 10 años, y su devoto perro Shakey se mudan a una pequeña ciudad de Chicago y al no leer la letra pequeña de su contrato de alquiler, JT se ve obligado a tratar de deshacerse de su perro."
            },
            {
                "titulo": "Shelby",
                "metadatos": [
                    "TV-G",
                    "Children & Family",
                    "1hr 32 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/5fad4a7f8b78ef001aa27bcd/details?lang=en",
                "descripcion": "Shelby es un perro sin dueño que tiene por costumbre fugarse de la perrera cada vez que tiene la oportunidad. Durante una de sus escapadas conoce a Jake, un niño que sueña con ser un gran mago, y se hacen amigos inseparables."
            },
            {
                "titulo": "Chiguagua: el fantasma",
                "metadatos": [
                    "TV-PG",
                    "Children & Family",
                    "1hr 22 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/62bcab10e9e8c00013709d5a/details?lang=en",
                "descripcion": "Al heredar una antigua casa de vacaciones, los Fastener se dan cuenta que la perra de sus antepasados, Sophie los persigue. Homer, su golden retriever, se hace amigo de Sophie y descubre que ella solo está buscando una familia a la que amar"
            },
            {
                "titulo": "Max salva al Mundo",
                "metadatos": [
                    "Children & Family",
                    "1hr 28 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/60c8abd436537d0013320af4/details?lang=en",
                "descripcion": "Sean y su perro Max quieren ser detectives pero en su vecindario no sucede nada hasta que desaparece un diamante. Ahora tendrán que enfrentarse a un grupo de alienígenas que vienen al planeta con planes de quemar la Tierra."
            },
            {
                "titulo": "Benny , El Feo",
                "metadatos": [
                    "TV-PG",
                    "Children & Family",
                    "1hr 39 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/62bf09238672a30013bd7ef8/details?lang=en",
                "descripcion": "Es la historia de un perro sin buena apariencia, sus dueños no tenian idea de que hacer con el cachorro extraño. Pero su ternura logro que una familia lo adoptara y desde ese momento la vida de Benny ha cambiado totalmente."
            },
            {
                "titulo": "Un amor hasta las patas",
                "metadatos": [
                    "TV-PG",
                    "Comedy",
                    "1hr 26 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/603e6222049634001a5f3418/details?lang=en",
                "descripcion": "Su amiga Roxana decide conseguirle una cita a través de las redes sociales. El desastre de la cita la lleva a pedirle un deseo a un mágico \"gato de los deseos\": tener un novio tan tierno y comprensible como sus 2 adorables perros."
            },
            {
                "titulo": "Mi Angel Guardián",
                "metadatos": [
                    "TV-PG",
                    "Children & Family",
                    "1hr 25 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/60c8abc136537d0013320966/details?lang=en",
                "descripcion": "Cooper, un perro, es el único sobreviviente de un terrible accidente automovilístico. Jake pierde a su esposa e hijos en el accidente. Jake es de enojo hacia el perro, pero este vinculo termina siendo lo unico que lo ayuda a seguir viviendo."
            },
            {
                "titulo": "Amor por el Perro",
                "metadatos": [
                    "Children & Family",
                    "1hr 21 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/5fda4095aabcdd001aaf4430/details?lang=en",
                "descripcion": "Cuando una madre divorciada intenta iniciar una nueva relación, sus hijos y su perro comienzan a sabotear el romance. Tienen éxito, hasta que aparece un ex novio de la escuela."
            },
            {
                "titulo": "¿EI, Dónde está mi Perro?",
                "metadatos": [
                    "TV-PG",
                    "Children & Family",
                    "1hr 22 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/5fda414b0dddaf0013b83734/details?lang=en",
                "descripcion": "Un joven llamado Ray se queda en casa para cuidar al perro de la familia, Harry, para demostrarles a sus padres que no es, como dicen, \"irresponsable\"."
            },
            {
                "titulo": "El refugio",
                "metadatos": [
                    "TV-PG",
                    "Children & Family",
                    "1hr 24 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/62ffebd0c24630001a8b226c/details?lang=en",
                "descripcion": "La familia Davis es un desastre, pero un perro callejero logrará en poco tiempo restaurar su matrimonio, arreglar una relación padre-hijo deteriorada, alegrar la vida de un niño de 9 años y salvar a un niño muy pequeño."
            },
            {
                "titulo": "Un equipo incomparable",
                "metadatos": [
                    "TV-PG",
                    "Children & Family",
                    "1hr 20 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/62fe9e866df8ae001a0464ae/details?lang=en",
                "descripcion": "Seeker, un perro que no puede oler, y Fetch, un cerdo casi ciego ayudan a mascotas perdidas a encontrar sus hogares."
            },
            {
                "titulo": "De patitas a la calle",
                "metadatos": [
                    "TV-G",
                    "Children & Family",
                    "1hr 23 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/60e459453988a50013b7617f/details?lang=en",
                "descripcion": "Una perra llamada Lasmi se perdió en la ciudad de Lima. Un grupo de patrulla canina la ayuda a encontrar a su familia. Pero un grupo de traficantes está secuestrando perros, por lo que deben descubrirlos y atraparlos."
            },
            {
                "titulo": "K-9 Aventuras: Un Cuento de Navidad",
                "metadatos": [
                    "TV-G",
                    "Children & Family",
                    "1hr 29 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/61f2a44d04ff25001a4fe790/details?lang=en",
                "descripcion": "Kassie, sus amigos y su perro, Scoot, organizan una recaudación de fondos para las fiestas, pero deben proteger el dinero de algunos ladrones para poder salvar la Navidad."
            },
            {
                "titulo": "Smitty",
                "metadatos": [
                    "TV-PG",
                    "Children & Family",
                    "1hr 34 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/60c8abbc36537d00133208f2/details?lang=en",
                "descripcion": "Ben, un chico de trece años, lleva a cabo continuas travesuras que traen de cabeza a su madre, una mujer soltera que lucha cada día por intentar salir adelante sin una pareja que le ayude a tratar que el comportamiento de su hijo mejore."
            },
            {
                "titulo": "La Mejor Amiga de Summer",
                "metadatos": [
                    "Children & Family",
                    "1hr 41 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/60bf7276d782df0013ef296c/details?lang=en",
                "descripcion": "El brillante e independiente Summer Larsen, de 12 años, rescata a un dulce perro callejero y no se detendrá ante nada para salvarlo. Y es su determinación lo que finalmente impacta a quienes la rodean."
            },
            {
                "titulo": "El perrito Pudsey",
                "metadatos": [
                    "PG",
                    "Children & Family",
                    "1hr 27 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/5f7b86a0e4b56900138b713a/details?lang=en",
                "descripcion": "En la ciudad de Londres Pudsey es feliz con su vida de perro callejero, pero un día su vida cambiará radicalmente. Molly, George y Tommy son tres hermanos que deciden acogerlo en la familia. Todo cambia tras la muerte de su padre."
            },
            {
                "titulo": "El Sol de Medianoche",
                "metadatos": [
                    "TV-PG",
                    "Children & Family",
                    "1hr 36 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/60bf7226d782df0013ef25df/details?lang=en",
                "descripcion": "En las heladas tierras del norte de Canadá, el joven Luke desafiará los peligros de la naturaleza y la dura inclemencia del tiempo invernal para ayudar a un joven oso polar a que se reúna con su madre."
            },
            {
                "titulo": "Una verdadera amistad",
                "metadatos": [
                    "Children & Family",
                    "1hr 30 min",
                    "There are no inadequacies"
                ],
                "link": "https://pluto.tv/latam/on-demand/movies/5fda409aaabcdd001aaf44a0/details?lang=en",
                "descripcion": "Finn es un niño de 13 años que es acosado constantemente en la escuela, pero su vida comienza a cambiar el día que conoce a un labrador llamado Marshall, que vive en condiciones extremas y necesita atención médica."
            }
        ]
    },
```
</details>

---

### De la seccion LiveTV:
- Traer todos los canales

### De ambas secciones:
- Guardar la información obtenida en una base de datos, en archivo .json
- Imprimir el tiempo de ejecución en el script

### Plus:
De la sección LiveTV:

Traer la grilla de contenidos con sus
- titulo
- horarios
- link

### De la seccion On Demand:
- Episodios de cada serie.
- Metadata de los episodios.
- Identificar modelo de negocio.

### De ambas secciones:
- Si es posible obtener mas información/metadata por cada contenido.
- Analisis y/o limpieza de Metadata.
- Otros campos que consideren relevantes
- Tiempo de ejecución menor a 2hs.
