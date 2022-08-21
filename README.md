# US Stock Analyser

Stock analyser is a tool for getting recommendation and stock information from Yahoo Finance. It's built to be a SoftUni
project without any commercial purposes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

The project consists of several endpoints:
```
    '/register' - Register a user, returns a token
    '/login' - Login, returns a token
    '/recommendation' - Returns a recommendation, requires ticker and token for authorization.
    '/balancesheet' - Returns balance sheet view, requires ticker and token, premium users only
    '/analysis' - Returns forecast, premium users only
    '/upgrade' - interacts with strypes for an account upgrade
    '/success_payment' -  being handled after a successful payment
    '/failed_payment' - being handled after failed payment
    '/webhook' - should be developed if the app is released to handle payments
    '/view_my_analysis' - views user analysis performed, requires token
```

## Developers
* Kiril Spiridonov