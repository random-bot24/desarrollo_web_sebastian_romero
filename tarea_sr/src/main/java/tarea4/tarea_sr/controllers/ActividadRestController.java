package tarea4.tarea_sr.controllers ;
import tarea4.tarea_sr.models.Actividad;
import tarea4.tarea_sr.models.Nota; // Asumiendo que guardaste el DTO en un paquete 'dto'
import tarea4.tarea_sr.models.ActividadRepository;
import tarea4.tarea_sr.models.NotaRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/actividades")
public class ActividadRestController {

    @Autowired
    private ActividadRepository actividadRepository;

    @Autowired
    private NotaRepository notaRepository;

    // Buscador de actividades
    @GetMapping("/buscar")
    public ResponseEntity<?> buscarActividades(@RequestParam("q") String query) {
        // Validamos que el usuario haya escrito al menos 3 caracteres 
        if (query == null || query.trim().length() < 3) {
            return ResponseEntity.badRequest().body("La búsqueda debe tener al menos 3 caracteres.");
        }

        // Buscamos en la base de datos usando el método personalizado
        List<Actividad> resultadosDB = actividadRepository.buscarPorPatron(query);
        List<ActividadDTO> resultadosLimpios = new ArrayList<>();

        // Iteramos para transformar cada Actividad 
        for (Actividad act : resultadosDB) {
            // Calculamos el promedio de la nota
            Double promedio = notaRepository.obtenerPromedioPorActividad(act.getId());
            
            // Si la actividad aún no ha sido evaluada, asignamos el valor "-" 
            String notaFormateada = (promedio != null) ? String.format("%.1f", promedio).replace(",", ".") : "-";

            // Armamos el DTO extrayendo los datos requeridos 
            ActividadDTO dto = new ActividadDTO(
                act.getId(),
                act.getMiembro().getNombre(),
                act.getDia(),
                act.getTipo(),
                act.getMiembro().getComuna().getNombre(),
                act.getNombre(),
                act.getDescripcion(),
                notaFormateada
            );
            
            resultadosLimpios.add(dto);
        }

        // Retornamos el JSON con la lista de resultados
        return ResponseEntity.ok(resultadosLimpios);
    }

    //Evaluar actividad
    @PostMapping("/{id}/evaluar")
    public ResponseEntity<?> evaluarActividad(@PathVariable("id") Integer idActividad, 
                                              @RequestParam("valorNota") Integer valorNota) {
        
        // 1. Validar que la nota sea un número entero entre 1 y 7, ambos inclusives 
        if (valorNota < 1 || valorNota > 7) {
            return ResponseEntity.badRequest().body("La nota debe estar entre 1 y 7.");
        }

        // 2. Buscar la actividad en la base de datos
        Optional<Actividad> actividadOpt = actividadRepository.findById(idActividad);
        
        if (actividadOpt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Actividad actividad = actividadOpt.get();

        // 3. Crear la nueva nota y guardarla asociada a la actividad 
        Nota nuevaNota = new Nota();
        nuevaNota.setNota(valorNota);
        nuevaNota.setActividad(actividad);
        
        notaRepository.save(nuevaNota);

        // 4. Recalcular la nota promedio actual 
        Double nuevoPromedio = notaRepository.obtenerPromedioPorActividad(idActividad);

        // 5. Devolver el nuevo promedio (lo enviamos al frontend para actualizar la interfaz) 
        return ResponseEntity.ok(nuevoPromedio);
    }
}