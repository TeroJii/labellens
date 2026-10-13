# LabelLens
An app for assigning class labels to images in a folder.

## Planned interaction workflow

1. Select folder
2. Scan supported image files
3. Enter permitted labels
4. Validate and create label controls
5. Display first image
6. Choose label
7. Store label in session
8. Automatically advance to next image
9. Repeat until all images are labelled
10. Export CSV

## UI layout plan

```text
+----------------------------------------------------------------+
| Image folder: C:\Temp\images                   [Choose folder] |
|                                                                |
| Permitted labels: [cat, dog, other]                            |
|                                                [Apply labels]  |
+-------------------------------------------+--------------------+
|                                           | Label              |
|                                           |                    |
|                                           | ( ) cat            |
|               IMAGE                       | ( ) dog            |
|               PREVIEW                     | ( ) other          |
|                                           |                    |
|                                           |                    |
|                                           | Progress           |
|                                           | 16 / 240 labelled  |
+-------------------------------------------+--------------------+
| IMG_0017.jpg                                                   |
|                                                                |
| [Previous]                         [Skip]              [Next]  |
|                                                                |
| [Save progress]                              [Export CSV]      |
+----------------------------------------------------------------+
```
