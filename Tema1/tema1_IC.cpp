// tema1_IC.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <string.h>
#include <string>
#include <fstream>
using namespace std;

ifstream fin("mesaj.in");

/*
	in aceasta functie transform textul de la input in text doar cu caractere, fara alte simboluri
*/
string plainText(string txt)
{
	const int n = txt.length();
	string aux;

	int lungime = 0;
	for (int i = 0; i < n; i++)
	{
		if (txt[i] >= 'a' && txt[i] <= 'z')
		{
			aux.push_back(txt[i]);
		}
		else if (txt[i] >= 'A' && txt[i] <= 'Z')
		{
			aux.push_back(txt[i] + 32);
		}
	}
	return aux;
}

/*
* in aceasta functie calculez a cata litera este, si am observat ca, scazand din codul ascii al literei mici pe care vreau sa o gasesc, codul literei z si mai scad inca un -1, obtin 25-a cata litera e ea defap, iar pentru ca nu recunoaste modulo unui numar negativ, adun acel numar cu minus la 26 pentru ca apoi va fi un nr pozitiv
*/
int aCataLitera(char c)
{
	return (26 + (c - 'z' - 1)) % 26;
}

/*
* aici voi cripta plaintextul cu ajutorul cheii
*/
string cypherText(string s, string k)
{
	string enc;
	int j = 0;
	for (int i = 0; i < s.length(); i++) {
		char c = (aCataLitera(s[i]) + aCataLitera(k[j])) % 26;
		c = c + 'A';
		enc.push_back(c);
		j++;
		if (j == k.length())
		{
			j = 0;
		}
	}

	return enc;
}


/*
* stiind textul criptat si cheia, cu ajutorul acestei metode aflu textul initial
*/
string decrypt(string plain, string key)
{
	string aux;
	int j=0;
	for (int i = 0; i < plain.length(); i++)
	{
		char c = (26 + aCataLitera(plain[i]+32) - aCataLitera(key[j]) )% 26;
		c = c + 'a';
		aux.push_back(c);
		j++;
		if (j == key.length())
		{
			j = 0;
		}
	}
	return aux;
}

/*
* in aceasta functie generez subsirul unui sir, incepand cu o anumita pozitie, mergend din k in k pasi
*/
string subsir(string enc, int k, int poz)
{
	string subsir;
	for (int i = poz; i < enc.length(); i += k)
	{
		subsir.push_back(enc[i]);
	}
	return subsir;
}

/*
* cu ajutorul acestei metode calculez de cate ori un caracter apare in criptotext
*/
int frecventaLitera(string subsir, char litera)
{
	int frecventa = 0;
	for (int i = 0; i < subsir.length(); i++)
	{
		if (subsir[i] == litera)
			frecventa++;
	}
	return frecventa;
}

double absIC(double ic)
{
	if (ic < 0.065)
	{
		return (0.065 - ic);
	}
	else {
		return (ic - 0.065);
	}
}

/*
* in aceasta metoda caut lungimea cheii, cu ajutorul indexului de coincidenta
*/
int keyLength(string enc)
{
	int k = 2;
	bool findKey = false;

	while (findKey == false)
	{
		cout << k << endl;
		int poz = 0;
		do {
			int literaVzitata[26] = { 0 };//ma asigur sa adun o singura data o litera
			string sir = subsir(enc, k, poz);
			cout << sir << ": ";
			double IC = 0.000;
			for (int i = 0; i < sir.length(); i++)
			{
				if (literaVzitata[(sir[i] - 13) % 26] == 0) //am facut aceasta operatie pentru a spune a cata litera este, in ordinea din alfabetul englez 
				{
					int f = frecventaLitera(sir, sir[i]);
					literaVzitata[(sir[i] - 13) % 26] = 1;
					IC = IC + ((double)((double)f / (double)sir.length()) * (double)(((double)f - 1.0) / ((double)sir.length() - 1.0)));
				}
			}
			cout << IC << " ";
			if (absIC(IC) <= 0.01) //aici verific IC-ul
			{
				poz++;
				if (poz == k)
				{
					findKey = true; //daca am gasit lungimea potrivita, afisez lungimea
					return k;
				}
			}
			else {
				k++; //daca nu se potriveste IC-ul, atunci voi cauta cu urmatoarea lungime
				poz = k + 1; //si de aici ies din intructiunea do_while, fara a o forta

			}
			cout << endl;
		} while (poz < k);
	}
}

/*
* de aceasta metoda ma folosesc in gasirea efectiva a cheii, shiftand fiecare litera a unui text, cu atatea pozitii mod 26 cat este cerut
*/
string shiftedSubsir(string s, int l)
{
	string aux;
	for (int i = 0; i < s.length(); i++)
	{
		int poz = (aCataLitera(s[i]+32) + l) % 26;
		aux.push_back(poz + 'A');
	}

	return aux;
}

/*
* in aceasta metoda caut efectiv cheia -- metoda din curs, slide 28  
*/

string findKey(int length, string enc)
{
	string key;
	char litereFrecventeEng[26] = { 'e','t','a','o','i','n','s','r','h','d','l','u','c','m','f','y','w','g','p','b','v','k','x','q','j','z' };
	double frecventaLitereEng[26] = { 12.02 , 9.10 , 8.12 , 7.68 , 7.31 , 6.95 , 6.28 , 6.02, 5.92, 4.32, 3.98, 2.99, 2.71, 2.61, 2.30, 2.11, 2.09, 2.03, 1.82, 1.49, 1.11, 0.69, 0.17, 0.11, 0.10, 0.07 };

	for (int k = 0; k < length; k++)
	{

		string sir = subsir(enc, length, k);
		double sumMax = 0.00;
		int c;
		for (int l = 0; l < 26; l++)
		{
			
			double sum = 0.0000;
			string shiftedSir = shiftedSubsir(sir, l); //shiftez subsirul cu 'l' pozitii
			for (int i = 0; i < 26; i++)
			{
				double operatie = (double)(frecventaLitereEng[i] * ((double)frecventaLitera(shiftedSir, (i + 'A')) / (double)shiftedSir.length()));
				sum = (double)sum + (double)operatie;
			}
			if (sum > sumMax)
			{
				sumMax = sum; //cea mai mare suma
				c = l;
			}
		}
		c = (26 - c) % 26; //a k a litera a cheii
		key.push_back(c + 'a');

	}

	return key;
}


int main()
{
	cout << "Aici incepe criptarea\n";
	string mesaj;
	cout << "Cititi mesajul!\n ";
	getline(fin, mesaj);
	cout <<endl<< "Mesajul initial:" << endl << mesaj << endl;
	string plaintext = plainText(mesaj);
	cout << plaintext<<" "<<plaintext.length() << endl;

	string key;
	cout << endl << "dati cheia: " << endl;
	cin >> key;

	string cyphertext = cypherText(plaintext, key);
	cout << cyphertext << endl;

	cout << endl<<"Textul initial stiind cheia:" << endl << decrypt(cyphertext, key) << endl;
	int key_l = keyLength(cyphertext);
	cout << endl << "Key length: " << key_l << endl;

	string findedKey = findKey(key_l, cyphertext);
	cout << findedKey << endl;

	return 0;
}

/*
* obs! codul, in forma actuala, nu imi gaseste toata cheia
* gaseste lungimile lor, dar nu toata cheia
* 
* pentru urmatoarele chei outputul este:
* ->abc: 3 efc
* -> abba: 4 affa
*/

