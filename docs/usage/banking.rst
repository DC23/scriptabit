Banking
-------

The banking plugin automates the
`Gold Bank custom reward <http://habitica.wikia.com/wiki/Sample_Custom_Rewards#Creating_a_Gold_Bank>`_,
allowing you to check your balance, and make deposits or withdrawals.

The first time the banking plugin runs it will create a custom reward called
`Gold Bank`.
You can edit the name of the custom reward in Habitica once it has been created,
but do not change the task alias.

Do not delete the custom reward without first withdrawing all the gold, or your
gold will be lost.

Also, don't purchase the bank reward in Habitica. The current balance is shown
as the reward value for convenience. Actually purchasing the reward in-game will
cost gold equal to the bank balance, but will not update the actual balance
(although you could do this manually if required - simply edit the extra notes
field in the reward).

The primary advantage of using a bank is that the gold is not lost on death.
However, to maintain some balance the scriptabit bank charges
:ref:`banking-fees` on each transaction.

Gold, Mana, and Health Banks
++++++++++++++++++++++++++++

Since version 1.15.0, scriptabit banking supports mana and health banks in 
addition to the gold bank. These work identically to the gold bank except for 
the following:

- You must specify the bank type on the command line. ``sb-banking --bank-type mana``
  or ``sb-banking --bank-type health``.
- Each bank is stored in a separate custom reward.
- Fees are charged on a different scale. Health fees have a max of 5, and mana
  fees a max of 20. These are not adjustable through the program options.
- Your health cannot be set below 1 or above 50. In fact, due to the fees, you 
  probably can't get health above 49.
- Mana withdrawals are capped so you cannot exceed your maximum mana (based on
  intelligence).
- The bank tax option is only available for the gold bank.

Checking your balance
+++++++++++++++++++++

The simplest way to check your balance is through one of the Habitica apps or
the website. The current balance is stored in both the extra notes field, and in
the reward value.

To check your balance with scriptabit::

    sb-banking -b

There are no fees for balance checks.

Deposits
++++++++

Deposits are made with the `--bank-deposit` argument::

    scriptabit --run banking --bank-deposit 100

Or using the shortcut method (short-form arguments and banking command)::

    sb-banking -d 100

Deposits are capped by your available gold, so trying to deposit more gold than
you have is a simple way to deposit all your gold.

Withdrawals
+++++++++++

Withdrawals are made with the `--bank-withdraw` argument::

    scriptabit --run banking --bank-withdraw 100

Or using the shortcut method (short-form arguments and banking command)::

    sb-banking -w 100

Withdrawals are capped by the bank balance, so trying to withdraw more gold than
you have is a simple way to withdraw all gold from the bank.

Paying Taxes
++++++++++++

*Note that taxes only work for gold banks, not mana or health*

The banking plugin allows you to pay taxes. The gold will be deducted first from
your gold balance and then from the bank if required. This may be of use to
players seeking an extra challenge::

    scriptabit --run banking --bank-tax 100

Or using the shortcut method (short-form arguments and banking command)::

    sb-banking --bank-tax 100

.. _banking-fees:

Bank Fees
+++++++++

Extra realism is available through bank fees. Fees are charged for deposits and
withdrawals. Small transactions are expensive, with larger transactions becoming
better value for money. The fees level off significantly after 1000 gold.
This means that the most cost effective way to use the bank is to save at least
1000 gold first, however this increases the risk of losing your gold due to
death. It is up to you to balance the transaction cost with the risk of death.

The command line argument `bank-max-fee` sets the upper limit on fees.
Values up to 600 will make transactions very expensive, while going beyond
600 will start to make small transactions cost more than the transaction
amount.

Fees can be disabled by setting `bank-max-fee` to zero.
This can be on the command line, or permanently by adding the following
to the scriptabit.cfg file::

    [banking]
    bank-max-fee = 0
