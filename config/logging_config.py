# Definition des Logging-Setups für die gesamte Anwendung. Das Level kann hier angepasst werden, wenn das System in Produktion geht, um weniger detaillierte Logs zu erhalten. 
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.WARNING, # Standard-Log-Level auf WARNING setzen, um weniger detaillierte Logs in Produktion zu erhalten
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
