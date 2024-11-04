import ccxt
import time

# Configuration des clés API pour Binance, Kraken et Crypto.com
binance_api_key = 'lZpO7N3imurDzkSLE0OG7czCKlrN8FlX15pkJkWaRaOFa4c4MABwa69UmQeksfSN'
binance_secret_key = '9T5Zes1BfNBQp6Pruari6N4vNMvtPVcXdWVw1aZmDTLlk0FEHMsRo4r2stYL0ZYN'
kraken_api_key = 'rmqfPMFsJRbByR8dB90AsIbnJmYf7tpPLV22xpN3sbSkee7HdagOwgTy'
kraken_secret_key = 'gq5GNPLS+1IAD4KUJVma+l82OEfrVoVruBc9EEj4A4kFONU5EuF0dtU6yOW7aSzKS1km6peMkvYM3gYKMd4ACg=='

# Initialiser les exchanges
binance = ccxt.binance({
    'apiKey': binance_api_key,
    'secret': binance_secret_key,
})

kraken = ccxt.kraken({
    'apiKey': kraken_api_key,
    'secret': kraken_secret_key,
})

# Définir les frais de transaction pour chaque exchange (exprimés en pourcentage)
binance_fee = 0.001  # 0.1%
kraken_fee = 0.001    # 0.1%

# Fonction pour obtenir le prix d'une crypto-monnaie à partir de Binance et Kraken
def get_prices(crypto_symbol):
    prices = {}

    # Prix de Binance
    binance_price = binance.fetch_ticker(f'{crypto_symbol}/USDT')['last']
    prices['Binance'] = binance_price

    # Prix de Kraken
    kraken_price = kraken.fetch_ticker(f'XXBTZUSD')['last']
    print("Kraken price:", kraken_price)
    prices['Kraken'] = kraken_price

    return prices

# Fonction pour ajuster les prix en fonction des frais de transaction
def adjust_prices(prices, fees):
    adjusted_prices = {}
    for exchange, price in prices.items():
        if exchange == 'Binance':
            adjusted_prices[exchange] = price * (1 + fees['binance'])
        elif exchange == 'Kraken':
            adjusted_prices[exchange] = price * (1 + fees['kraken'])
    return adjusted_prices

# Fonction d'arbitrage
def arbitrage_opportunity(crypto_symbol):
    fees = {
        'binance': binance_fee,
        'kraken': kraken_fee,
    }

    while True:
        prices = get_prices(crypto_symbol)
        print("Prix des exchanges:", prices)

        # Ajuster les prix en fonction des frais de transaction
        adjusted_prices = adjust_prices(prices, fees)
        print("Prix ajustés (avec frais):", adjusted_prices)

        # Trouver les prix maximum et minimum ajustés
        max_exchange = max(adjusted_prices, key=adjusted_prices.get)
        min_exchange = min(adjusted_prices, key=adjusted_prices.get)
        amount_to_trade = 0.01
        # Calculer le profit potentiel
        min_price = adjusted_prices[min_exchange]
        max_price = adjusted_prices[max_exchange]
        profit = (max_price * amount_to_trade) - (min_price * amount_to_trade)

        # Vérification des opportunités d'arbitrage
        if profit > 1:
            ##amount_to_trade = 0.01  # Montant à acheter/vendre (ajustez selon votre capital)
            print(f"Arbitrage détecté! Acheter sur {min_exchange} à {min_price * amount_to_trade} et vendre sur {max_exchange} à {max_price * amount_to_trade}. Profit potentiel: {profit} USD")

            # Exécution des ordres
            if min_exchange == 'Binance':
                # Acheter sur Binance
                ## binance.create_market_buy_order(f'{crypto_symbol}/USDT', amount_to_trade)
                print(f"Achat de {amount_to_trade} {crypto_symbol} sur Binance.")

                # Vendre sur Kraken
                ## kraken.create_market_sell_order(f'X{crypto_symbol}ZUSD', amount_to_trade)
                print(f"Vente de {amount_to_trade} {crypto_symbol} sur Kraken.")

            elif min_exchange == 'Kraken':
                # Acheter sur Kraken
                ## kraken.create_market_buy_order(f'X{crypto_symbol}ZUSD', amount_to_trade)
                print(f"Achat de {amount_to_trade} {crypto_symbol} sur Kraken.")

                # Vendre sur Binance
                ## binance.create_market_sell_order(f'{crypto_symbol}/USDT', amount_to_trade)
                print(f"Vente de {amount_to_trade} {crypto_symbol} sur Binance.")

        else:
            print("Aucune opportunité d'arbitrage détectée.")

        # Attendre avant de vérifier à nouveau
        time.sleep(10)  # Vérifier toutes les 10 secondes

if __name__ == "__main__":
    crypto_symbol = "BTC"  # Remplacez par la crypto-monnaie que vous souhaitez surveiller
    arbitrage_opportunity(crypto_symbol)
