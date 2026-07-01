package tarea4.tarea_sr.models;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface ActividadRepository extends JpaRepository<Actividad, Integer> {

    @Query("SELECT a FROM Actividad a WHERE " +
           "LOWER(a.nombre) LIKE LOWER(CONCAT('%', :texto, '%')) OR " +
           "LOWER(a.descripcion) LIKE LOWER(CONCAT('%', :texto, '%')) OR " +
           "LOWER(a.miembro.comuna.nombre) LIKE LOWER(CONCAT('%', :texto, '%'))")
    List<Actividad> buscarPorPatron(@Param("texto") String texto);
}
