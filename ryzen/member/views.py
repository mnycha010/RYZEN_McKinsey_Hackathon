from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from stokvel.models import Stokvel
from .models import Member, FinancialRecord
from .forms import OnboardForm
from datetime import date, timedelta
 
from django.db.models import Sum
from django.core.paginator import Paginator



def onboard_view(request):
    """
    Registration / Onboarding view:
    - Creates a User
    - Creates a Member profile
    - Links to a Stokvel by ID
    - Creates an initial FinancialRecord
    """
    if request.method == "POST":
        form = OnboardForm(request.POST)
        if form.is_valid():
            # Create user
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create member profile
            member = form.save(commit=False)
            member.user = user

            # Link stokvel by alphanumeric ID
            stokvel_id = form.cleaned_data["stokvel_id"]
            try:
                stokvel = Stokvel.objects.get(id=stokvel_id, active=True)
            except Stokvel.DoesNotExist:
                messages.error(request, "Stokvel ID not found or inactive.")
                user.delete()  # clean up created user
                return redirect("member:onboard")

            member.stokvel = stokvel
            member.save()

            # Add member to stokvel's member list
            stokvel.members.add(member)

            # Create initial financial record
            FinancialRecord.objects.create(member=member, amount_saved=0.0, amount_borrowed=0.0)

            messages.success(request, f"Account created! You have joined {stokvel.name}. Please login.")
            return redirect("core:login")
    else:
        form = OnboardForm()

    return render(request, "member/onboard.html", {"form": form})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from member.models import Member, FinancialRecord
from stokvel.models import Stokvel

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect("core:login")

    member = Member.objects.filter(user=request.user).first()
    if not member or not member.stokvel:
        messages.info(request, "You are not part of any stokvel. Please join one.")
        return redirect("onboard")

    stokvel = member.stokvel
    contributions = FinancialRecord.objects.filter(member__stokvel=stokvel)

    # Total balance
    total_balance = sum(c.amount_saved for c in contributions)

    # Member contribution for current month
    today = date.today()
    member_contribution_record = contributions.filter(
        member=member,
        contribution_date__month=today.month,
        contribution_date__year=today.year
    ).first()
    member_contribution = member_contribution_record.amount_saved if member_contribution_record else 0

    total_members = stokvel.members.count()
    active_members_count = stokvel.members.filter(user__is_active=True).count()
    next_meeting_date = date(today.year, today.month, 15)  # Example: 15th of the month

    target_amount = total_members * stokvel.monthly_contribution
    current_month_total = sum(
        c.amount_saved for c in contributions
        if c.contribution_date.month == today.month and c.contribution_date.year == today.year
    )
    progress_percentage = int((current_month_total / target_amount) * 100) if target_amount else 0
    remaining_amount = target_amount - current_month_total
    remaining_label = "Surplus" if remaining_amount < 0 else "Remaining"

    # ----------------------------
    # Members with totals
    # ----------------------------
    members_data = []
    for m in stokvel.members.all():
        total_saved = m.financial_records.aggregate(total_saved=Sum('amount_saved'))['total_saved'] or 0
        amount_owed = max(stokvel.monthly_contribution - total_saved, 0)
        members_data.append({
            'member': m,
            'total_saved': total_saved,
            'amount_owed': amount_owed,
        })

    # Split active/inactive members
    active_members = [m for m in members_data if m['member'].user.is_active]
    inactive_members = [m for m in members_data if not m['member'].user.is_active]

    # ----------------------------
    # Pagination for active members
    # ----------------------------
    paginator = Paginator(active_members, 5)  # 5 members per page
    page_number = request.GET.get('page', 1)
    active_members_page = paginator.get_page(page_number)

    # ----------------------------
    # Chart Data (mock for testing)
    # ----------------------------
    # Income & Expense (Last 6 Months)
    months = []
    income_data = []
    expense_data = []
    for i in reversed(range(6)):
        dt = today - relativedelta(months=i)
        months.append(dt.strftime("%b %Y"))
        income_data.append(1000 + i*200)   # mock income
        expense_data.append(500 + i*150)   # mock expense

    # Savings Growth Trend (Past 12 Months)
    savings_growth_labels = []
    savings_growth_data = []
    cumulative_savings = 0
    for i in reversed(range(12)):
        dt = today - relativedelta(months=i)
        savings_growth_labels.append(dt.strftime("%b %Y"))
        cumulative_savings += 500 + i*50  # mock cumulative savings
        savings_growth_data.append(cumulative_savings)

    # Loan Repayment Trend (Past 12 Months)
    loan_repayment_labels = savings_growth_labels.copy()
    cumulative_loans = 0
    loan_repayment_data = []
    for i in reversed(range(12)):
        cumulative_loans += 200 + i*30  # mock loans
        loan_repayment_data.append(cumulative_loans)

    context = {
        "member": member,
        "stokvel": stokvel,
        "total_balance": total_balance,
        "member_contribution": member_contribution,
        "active_members_count": active_members_count,
        "total_members": total_members,
        "next_meeting_date": next_meeting_date,
        "progress_percentage": progress_percentage,
        "target_amount": target_amount,
        "remaining_amount": abs(remaining_amount),
        "remaining_label": remaining_label,
        "current_month_total": current_month_total,
        "active_members_page": active_members_page,
        "inactive_members": inactive_members,
        "months": months,
        "income_data": income_data,
        "expense_data": expense_data,
        "savings_growth_labels": savings_growth_labels,
        "savings_growth_data": savings_growth_data,
        "loan_repayment_labels": loan_repayment_labels,
        "loan_repayment_data": loan_repayment_data,
        "net_arrears": sum(m['amount_owed'] for m in members_data),
    }

    return render(request, "member/dashboard.html", context)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from datetime import date
import cohere

from .models import Member

COHERE_API_KEY = "I8HCAXrT6Yd71scv5EUWad2YbeTTFEsLvQj3IhlQ"
co = cohere.Client(COHERE_API_KEY)


def ai_analytics_view(request):
    if not request.user.is_authenticated:
        return redirect("core:login")

    member = Member.objects.filter(user=request.user).first()
    if not member or not member.stokvel:
        messages.info(request, "You are not part of any stokvel. Please join one.")
        return redirect("onboard")

    stokvel = member.stokvel

    # Retrieve chat history from session, or start new
    chat_history = request.session.get("chat_history", [])

    if request.method == "POST":
        query = request.POST.get("query")

        # Add the user's query to chat history
        chat_history.append({"role": "user", "content": query})

        # Build database context
        financial_data = []
        for m in stokvel.members.all():
            total_saved = m.financial_records.aggregate(total_saved=Sum('amount_saved'))['total_saved'] or 0
            total_borrowed = m.financial_records.aggregate(total_borrowed=Sum('amount_borrowed'))['total_borrowed'] or 0
            financial_data.append(
                f"{m.user.get_full_name()}: Saved R{total_saved}, Borrowed R{total_borrowed}"
            )

        db_context = "\n".join(financial_data)

        try:
            chat_response = co.chat(
                model="c4ai-aya-expanse-32b",
                message=f"""
                    You are a stokvel financial assistant. Answer the user's query **directly and clearly**.
                    Do NOT mention "Based on the database" or "database context" in your response.
                    Do NOT use any markdown formatting (no ** or __).

                    User query:
                    {query}

                    Relevant data (for internal reference, do not include in the response):
                    {db_context}
                    """,
                max_tokens=250,
                temperature=0.6
            )

            ai_reply = chat_response.text
        except Exception as e:
            ai_reply = f"Error: {str(e)}"

        # Add AI response to chat history
        chat_history.append({"role": "assistant", "content": ai_reply})

        # Save updated chat history in session
        request.session["chat_history"] = chat_history
        request.session.modified = True

    context = {
        "member": member,
        "stokvel": stokvel,
        "chat_history": chat_history,
    }

    return render(request, "member/ai_analytics.html", context)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt  # only for testing; better to pass CSRF token in fetch headers
def ai_analytics_clear(request):
    if request.method == "POST":
        if "chat_history" in request.session:
            del request.session["chat_history"]
            request.session.modified = True
        return JsonResponse({"status": "cleared"})
    return JsonResponse({"status": "failed"}, status=400)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from member.models import Member, FinancialRecord

@login_required
def profile_view(request):
    user = request.user
    member = Member.objects.filter(user=user).first()

    if not member:
        return redirect("onboard")  # Or show a message if no member profile

    stokvel = member.stokvel

    # Aggregated data
    total_saved = member.financial_records.aggregate(total=Sum('amount_saved'))['total'] or 0
    total_borrowed = member.financial_records.aggregate(total=Sum('amount_borrowed'))['total'] or 0
    total_arrears = max(total_borrowed - total_saved, 0)

    context = {
        "user": user,
        "member": member,
        "stokvel": stokvel,
        "total_saved": total_saved,
        "total_borrowed": total_borrowed,
        "total_arrears": total_arrears,
    }

    return render(request, "member/profile.html", context)

def meetings_view(request):
    return render(request, "member/meetings.html")