from repositories.indicator_repository import IndicatorRepository


class PurchasingPowerService:

    CPI_INDICATOR = "FP.CPI.TOTL"
    PPP_INDICATOR = "PA.NUS.PPP"

    def __init__(
        self,
        repository: IndicatorRepository
    ):
        self.repository = repository

    def adjust_for_inflation(
        self,
        amount: float,
        country_code: str,
        source_year: int,
        target_year: int
    ) -> float:

        if amount < 0:
            raise ValueError(
                "Amount cannot be negative."
            )

        source_cpi = self.repository.get_value(
            country_code,
            self.CPI_INDICATOR,
            source_year,
        )

        target_cpi = self.repository.get_value(
            country_code,
            self.CPI_INDICATOR,
            target_year,
        )

        adjusted_amount = (
            amount
            * target_cpi
            / source_cpi
        )

        return adjusted_amount

    def convert_to_international_dollars(
        self,
        amount: float,
        country_code: str,
        year: int
    ) -> float:
        
        if amount < 0:
            raise ValueError(
                "Amount cannot be negative."
                )
        
        ppp = self.repository.get_value(
            country_code,
            self.PPP_INDICATOR,
            year,
            )
        
        international_dollars = amount / ppp

        return international_dollars
    
    def to_target_year_international_dollars(
        self,
        amount: float,
        country_code: str,
        source_year: int,
        target_year: int
    ) -> float:
        
        inflation_adjusted_amount = self.adjust_for_inflation(
            amount,
            country_code,
            source_year,
            target_year,
            )
        
        international_dollars = (
            self.convert_to_international_dollars(
                inflation_adjusted_amount,
                country_code,
                target_year,
            )
        )

        return international_dollars