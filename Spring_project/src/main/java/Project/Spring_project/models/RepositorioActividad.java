package Project.Spring_project.models;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.time.LocalDateTime;
import java.util.List;


public interface RepositorioActividad extends JpaRepository<Actividad, Long>{
    @Query ("SELECT a FROM Actividad a Where a.fechaTermino< :ahora")
    List<Actividad> findActividadesFinalizadas(LocalDateTime ahora);
}
